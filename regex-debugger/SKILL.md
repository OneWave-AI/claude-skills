---
name: regex-visual-debugger
description: Debug regex patterns with visual breakdowns, plain English explanations, test case generation, and flavor conversion. Use when user needs help with regular expressions or pattern matching.
---

# Regex Visual Debugger

Interactive regex testing, explanation, and debugging tool.

## When to Use This Skill

Activate when the user:
- Provides a regex pattern to debug
- Asks "why isn't my regex working?"
- Needs a regex pattern explained
- Wants to test regex against strings
- Asks to convert regex between flavors (Python, JS, etc.)
- Needs regex pattern suggestions
- Mentions regular expressions or pattern matching

## Instructions

1. **Analyze the Regex Pattern**
   - Parse the regex structure
   - Identify each component (groups, quantifiers, character classes)
   - Check for common syntax errors
   - Validate regex syntax for specified flavor

2. **Provide Plain English Explanation**
   - Break down pattern piece by piece
   - Explain what each part matches
   - Describe overall pattern behavior
   - Clarify quantifier greediness
   - Explain capture groups vs. non-capturing groups

3. **Visual Breakdown**
   - Show pattern structure hierarchically
   - Highlight groups and alternations
   - Indicate character classes and ranges
   - Mark anchors and boundaries

4. **Test Against Examples**
   - Test provided test strings
   - Show what matches and what doesn't
   - Highlight matched portions
   - Explain why matches succeed or fail
   - Show capture group contents

5. **Identify Common Issues**
   - Unescaped special characters
   - Incorrect quantifiers
   - Greedy vs. non-greedy issues
   - Anchor misplacement
   - Unclosed groups
   - Flavor-specific incompatibilities

6. **Generate Test Cases**
   - Create strings that should match
   - Create strings that should NOT match
   - Include edge cases
   - Test boundary conditions

7. **Suggest Improvements**
   - More efficient patterns
   - More readable alternatives
   - Performance optimizations
   - Edge case handling

8. **Convert Between Flavors**
   - Python (re module)
   - JavaScript
   - Perl
   - Java
   - .NET
   - PHP (PCRE)

## Output Format

```markdown
# Regex Analysis: `pattern`

## Plain English Explanation
This pattern matches [description]:
- `^` - Start of string
- `[A-Z]` - One uppercase letter
- `\d{3}` - Exactly 3 digits
- `$` - End of string

**Overall**: Matches strings like "A123", "Z999"

## Visual Structure
```
^                 - Start anchor
[A-Z]            - Character class (uppercase letters)
\d{3}            - Digit, exactly 3 times
$                 - End anchor
```

## Test Results

### Matches
- `A123` -> Full match
- `Z999` -> Full match

### No Match
- `a123` -> Lowercase 'a' doesn't match [A-Z]
- `A12` -> Only 2 digits (needs 3)
- `A1234` -> Too many digits

## Capture Groups
1. Group 1: `[captured text]`
2. Group 2: `[captured text]`

## Issues Found
**Issue 1**: Pattern is too restrictive
- **Problem**: Doesn't handle lowercase letters
- **Fix**: Use `[A-Za-z]` instead of `[A-Z]`

## Suggested Improvements
```regex
# More flexible version
^[A-Za-z]\d{3,5}$
```
**Changes**:
- Added lowercase letters
- Changed `{3}` to `{3,5}` for 3-5 digits

## Generated Test Cases

### Should Match
```
A123
Z999
B456
```

### Should NOT Match
```
1ABC    (starts with digit)
ABCD    (no digits)
A12     (too few digits)
```

## Flavor-Specific Notes
**JavaScript**: [any JS-specific notes]
**Python**: [any Python-specific notes]

## Conversion to Other Flavors

### JavaScript
```javascript
const pattern = /^[A-Z]\d{3}$/;
const match = str.match(pattern);
```

### Python
```python
import re
pattern = r'^[A-Z]\d{3}$'
match = re.match(pattern, string)
```

## Performance Notes
- Current complexity: O(n)
- No backtracking issues
- Consider using non-capturing groups: `(?:...)` for better performance
```

## Examples

**User**: "Why doesn't this regex match emails: `\w+@\w+\.\w+`?"
**Response**: Analyze pattern → Explain it matches simple emails only → Show test cases (fails on "user+tag@domain.co.uk") → Identify issues (doesn't handle special chars, multiple TLDs) → Provide improved pattern → Generate comprehensive test cases

**User**: "Explain this regex: `^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$`"
**Response**: Break down pattern (IP address matcher) → Explain each component → Show it matches valid IPs (0-255 per octet) → Provide test cases → Visualize structure

**User**: "Convert this Python regex to JavaScript: `(?P<name>\w+)`"
**Response**: Identify named capture group (Python feature) → Convert to JS equivalent → Explain differences → Show both versions with usage examples

## Best Practices

- Always test regex with edge cases
- Explain in plain English first
- Show concrete examples (not just theory)
- Highlight common pitfalls for each pattern
- Provide both positive and negative test cases
- Consider performance implications
- Note flavor-specific features
- Suggest simpler alternatives when possible
- Use non-capturing groups for performance
- Escape special characters properly
- Be explicit about case sensitivity
- Test with Unicode characters if relevant
