
from django.db import models
import json

class Node(models.Model):
    type = models.CharField(max_length=20,  default='operand')  # Assuming type is a string like 'operator' or 'operand'
    left = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='left_child')
    right = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='right_child')
    value = models.CharField(max_length=100, blank=True, null=True)  # Optional value for operand nodes

    def __str__(self):
        return f"Node(type={self.type}, value={self.value})"


class Rule(models.Model):
    rule_string = models.TextField()
    ast = models.JSONField()  # Store the AST as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_string

