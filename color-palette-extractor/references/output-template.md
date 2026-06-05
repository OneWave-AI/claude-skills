# Output Template

Use this structure when reporting an extracted palette. Replace bracketed values with real data.

```
COLOR PALETTE EXTRACTOR

Source: [Image / Website URL]

----------------------------------------
PRIMARY PALETTE
----------------------------------------

1. Primary Color
   HEX: #3B82F6
   RGB: rgb(59, 130, 246)
   HSL: hsl(217, 91%, 60%)
   Usage: Main brand color, primary buttons, links
   Prominence: 32%

2. Secondary Color
   HEX: #0EA5E9
   RGB: rgb(14, 165, 233)
   HSL: hsl(199, 89%, 48%)
   Usage: Accent elements, hover states
   Prominence: 18%

3. Background
   HEX: #F8FAFC
   RGB: rgb(248, 250, 252)
   HSL: hsl(210, 40%, 98%)
   Usage: Page background, cards
   Prominence: 25%

4. Text Primary
   HEX: #1E293B
   RGB: rgb(30, 41, 59)
   HSL: hsl(217, 33%, 17%)
   Usage: Body text, headings
   Prominence: 15%

5. Accent
   HEX: #10B981
   RGB: rgb(16, 185, 129)
   HSL: hsl(158, 84%, 39%)
   Usage: Success states, CTAs
   Prominence: 10%

----------------------------------------
COLOR SCALE (Tailwind-style)
----------------------------------------

Primary:
  50:  #EFF6FF  [lightest]
  100: #DBEAFE
  200: #BFDBFE
  300: #93C5FD
  400: #60A5FA
  500: #3B82F6  [base]
  600: #2563EB
  700: #1D4ED8
  800: #1E40AF
  900: #1E3A8A  [darkest]
  950: #172554

----------------------------------------
COLOR HARMONY SCHEMES
----------------------------------------

Complementary:
  Base: #3B82F6 (blue)
  Complement: #F6823B (orange)

Analogous:
  #3B82F6 (blue)
  #3BF6D9 (cyan)
  #3B3BF6 (indigo)

Triadic:
  #3B82F6 (blue)
  #F6823B (orange)
  #82F63B (green)

----------------------------------------
ACCESSIBILITY CHECKS
----------------------------------------

Contrast Ratios (WCAG 2.1):

Text on Background:
  #1E293B on #F8FAFC: 14.2:1  AAA (excellent)

Primary on Background:
  #3B82F6 on #F8FAFC: 4.8:1  AA (good)

White text on Primary:
  #FFFFFF on #3B82F6: 4.6:1  AA (good)

Accent on Background:
  #10B981 on #F8FAFC: 3.2:1  AA Large text only

Recommendations:
- Use darker shade of accent for small text
- Primary button text should be white (#FFFFFF)
- Consider #047857 for better contrast

----------------------------------------
COLOR PSYCHOLOGY
----------------------------------------

Blue (#3B82F6):
- Trust, professionalism, calm
- Common for: Tech, finance, healthcare

Cyan (#0EA5E9):
- Clarity, innovation, energy
- Common for: SaaS, communications, modern brands

Green (#10B981):
- Growth, success, health
- Common for: Environmental, finance, wellness

----------------------------------------
DESIGN SYSTEM INTEGRATION
----------------------------------------

Suggested Usage:
- Primary: Main CTAs, links, active states
- Secondary: Secondary buttons, highlights
- Background: Page/card backgrounds
- Text: Body copy, headings
- Accent: Success messages, highlights

Color Roles:
- Success: #10B981 (green accent)
- Warning: #F59E0B (generate from palette)
- Error: #EF4444 (generate complement)
- Info: #3B82F6 (primary blue)
```
