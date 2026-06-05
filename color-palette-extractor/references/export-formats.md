# Export Formats

Provide the palette in whichever formats the request calls for. Default to CSS variables and Tailwind config when unspecified.

## CSS Variables

```css
:root {
  --color-primary: #3B82F6;
  --color-secondary: #0EA5E9;
  --color-background: #F8FAFC;
  --color-text: #1E293B;
  --color-accent: #10B981;
}
```

## Tailwind Config

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EFF6FF',
          500: '#3B82F6',
          900: '#1E3A8A',
        },
      }
    }
  }
}
```

## SCSS Variables

```scss
$primary: #3B82F6;
$secondary: #0EA5E9;
$background: #F8FAFC;
$text: #1E293B;
$accent: #10B981;
```

## JSON

```json
{
  "primary": "#3B82F6",
  "secondary": "#0EA5E9",
  "background": "#F8FAFC",
  "text": "#1E293B",
  "accent": "#10B981"
}
```

## Android XML

```xml
<color name="primary">#3B82F6</color>
<color name="secondary">#0EA5E9</color>
```

## iOS Swift

```swift
extension UIColor {
  static let primary = UIColor(hex: "3B82F6")
  static let secondary = UIColor(hex: "0EA5E9")
}
```
