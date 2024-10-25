from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Rule
import re
import json

import logging

logger = logging.getLogger(__name__)

class RuleEngineViewSet(viewsets.ViewSet):
    def index(self, request):
        # Fetch all rules to display on the index page
        rules = Rule.objects.all().values('id', 'rule_string')
        return render(request, 'rules/index.html', {'rules': rules})

    def create_rule(self, request):
        rule_string = request.data.get('rule_string')
        if not rule_string:
            return Response({"error": "Rule string is required."}, status=400)

        # Generate the AST from the rule string
        ast = self.generate_ast(rule_string)
        
        # Save the rule and its AST in the database
        rule = Rule(rule_string=rule_string, ast=ast)
        rule.save()

        # Fetch all rules again to update the dropdown
        rules = Rule.objects.all().values('id', 'rule_string')
        
        # Return the generated AST and updated rule list
        return Response({
            "ast": ast,
            "rules": list(rules)
        })

    @action(detail=False, methods=['POST'])
    def get_rules(self, request):
        # Fetch all rules for the frontend
        rules = Rule.objects.all().values('id', 'rule_string')
        return Response({"rules": list(rules)})

    @action(detail=False, methods=['POST'])
    def combine_rules(self, request):
        # Combine selected rules based on rule IDs
        rule_ids = request.data.get('rule_ids', [])
        if not rule_ids:
            return Response({"error": "No rules selected"}, status=400)

        # Fetch selected rules and combine them with "AND"
        rules = Rule.objects.filter(id__in=rule_ids)
        combined_string = " AND ".join(f"({rule.rule_string})" for rule in rules)
        
        # Generate AST from the combined string
        ast = self.generate_ast(combined_string)
        return Response({
            "combined_string": combined_string,
            "ast": ast
        })

    def generate_ast(self, rule_string):
        # Tokenize and parse the rule string into an AST
        tokens = self.tokenize(rule_string)
        return self.parse_tokens(tokens)

    def tokenize(self, rule_string):
        tokens = []
        i = 0
        while i < len(rule_string):
            char = rule_string[i]
            
            # Handle parentheses
            if char in '()':
                tokens.append(char)
                i += 1
                continue
            
            # Handle operators (AND, OR)
            if rule_string[i:i+3] == 'AND':
                tokens.append('AND')
                i += 3
                continue
            if rule_string[i:i+2] == 'OR':
                tokens.append('OR')
                i += 2
                continue
            
            # Handle conditions
            if char.isalnum() or char in '><= ':
                condition = ''
                while i < len(rule_string) and rule_string[i:i+3] != 'AND' and rule_string[i:i+2] != 'OR' and rule_string[i] not in '()':
                    condition += rule_string[i]
                    i += 1
                if condition.strip():
                    tokens.append(condition.strip())
                continue
            
            i += 1
        
        return tokens

    def parse_tokens(self, tokens):
        # Parse tokens into an AST
        def parse_expression():
            stack = []
            
            while tokens:
                token = tokens[0]
                
                if token == '(':
                    tokens.pop(0)
                    stack.append(parse_expression())
                elif token == ')':
                    tokens.pop(0)
                    break
                elif token in ('AND', 'OR'):
                    if len(stack) < 1:
                        raise ValueError("Invalid rule syntax: operator without operands")
                    
                    operator = tokens.pop(0)
                    left = stack.pop()
                    
                    if not tokens:
                        raise ValueError("Invalid rule syntax: operator without right operand")
                    
                    right = parse_expression() if tokens[0] == '(' else {
                        "type": "operand",
                        "value": tokens.pop(0)
                    }
                    
                    stack.append({
                        "type": "operator",
                        "value": operator,
                        "children": [left, right]
                    })
                else:
                    stack.append({
                        "type": "operand",
                        "value": tokens.pop(0)
                    })
            
            if not stack:
                raise ValueError("Invalid rule syntax: empty expression")
            
            while len(stack) > 1:
                right = stack.pop()
                operator = stack.pop()
                left = stack.pop()
                stack.append({
                    "type": "operator",
                    "value": operator,
                    "children": [left, right]
                })
            
            return stack[0]
        
        return parse_expression()

    def evaluate_rule(self, request):
        ast_data = request.data.get('ast', {})
        data = request.data.get('data', {})
        result = self.evaluate_ast(ast_data, data)
        return Response({'result': result})

    def evaluate_ast(self, ast_data, data):
        # Recursively evaluate the AST against input data
        logger.info(f"Evaluating AST Node: {ast_data}")
        
        if ast_data['type'] == 'operator':
            results = [self.evaluate_ast(child, data) for child in ast_data['children']]
            
            if ast_data['value'] == 'AND':
                logger.info(f"Evaluating AND: {results}")
                return all(results)
            elif ast_data['value'] == 'OR':
                logger.info(f"Evaluating OR: {results}")
                return any(results)
                
        elif ast_data['type'] == 'operand':
            condition = ast_data['value']
            variable, operator, value = self.parse_condition(condition)
            logger.info(f"Evaluating condition: {condition} with data: {data}")
            if None in (variable, operator, value):
                return False
                
            left_value = data.get(variable)
            logger.info(f"Variable {variable}: {left_value} {operator} {value}")
            if left_value is None:
                return False

            if operator == '>':
                return left_value > value
            elif operator == '!=':
                return left_value != value
            elif operator == '>=':
                return left_value >= value
            elif operator == '<':
                return left_value < value
            elif operator == '<=':
                return left_value <= value
            elif operator == '=':
                return left_value == value

        return False


    def parse_condition(self, condition):
        # Parse individual condition strings
        logger.info(f"Parsing condition: {condition}")
        match = re.match(r'(\w+)\s*([<>]=?|=)\s*(\d+)', condition)
        if match:
            variable = match.group(1)
            operator = match.group(2)
            value = int(match.group(3))
            logger.info(f"Parsed condition: variable={variable}, operator={operator}, value={value}")
            return variable, operator, value
        return None, None, None
