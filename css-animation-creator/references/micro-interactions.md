# Micro-interactions

## Button Effects

```tsx
// Press effect
<button className="transition-transform duration-100 active:scale-95">
  Click me
</button>

// Ripple effect (React)
function RippleButton({ children, ...props }) {
  const [ripples, setRipples] = useState([]);

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setRipples([...ripples, { x, y, id: Date.now() }]);
    setTimeout(() => setRipples(r => r.slice(1)), 600);
  };

  return (
    <button className="relative overflow-hidden" onClick={handleClick} {...props}>
      {ripples.map(ripple => (
        <span
          key={ripple.id}
          className="absolute bg-white/30 rounded-full animate-[ripple_0.6s_ease-out]"
          style={{
            left: ripple.x,
            top: ripple.y,
            transform: 'translate(-50%, -50%)'
          }}
        />
      ))}
      {children}
    </button>
  );
}
```

```css
@keyframes ripple {
  from {
    width: 0;
    height: 0;
    opacity: 0.5;
  }
  to {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}
```

## Hover Effects

```tsx
// Lift effect
<div className="transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
  Card content
</div>

// Glow effect
<button className="transition-shadow duration-300 hover:shadow-[0_0_20px_rgba(59,130,246,0.5)]">
  Glow button
</button>

// Border animation
<div className="relative group">
  <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg blur opacity-0 group-hover:opacity-75 transition duration-300" />
  <div className="relative bg-white rounded-lg p-6">Content</div>
</div>

// Underline animation
<a className="relative inline-block after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-current after:transition-all after:duration-300 hover:after:w-full">
  Animated link
</a>

// Fill animation
<a className="relative overflow-hidden group">
  <span className="relative z-10 transition-colors duration-300 group-hover:text-white">
    Hover me
  </span>
  <span className="absolute inset-0 bg-blue-600 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300" />
</a>
```

## Icon Animations

```tsx
// Rotate on hover
<button className="group">
  <SettingsIcon className="transition-transform duration-500 group-hover:rotate-180" />
</button>

// Bounce on hover
<button className="group">
  <ArrowIcon className="transition-transform group-hover:translate-x-1 group-hover:animate-bounce" />
</button>

// Scale + rotate
<button className="group">
  <PlusIcon className="transition-all duration-300 group-hover:scale-110 group-hover:rotate-90" />
</button>
```

## Form Interactions

```tsx
// Input focus effect
<div className="relative">
  <input
    className="peer w-full border-b-2 border-gray-300 focus:border-blue-600 outline-none py-2 transition-colors"
    placeholder=" "
  />
  <label className="absolute left-0 top-2 text-gray-500 transition-all peer-focus:-top-4 peer-focus:text-sm peer-focus:text-blue-600 peer-[:not(:placeholder-shown)]:-top-4 peer-[:not(:placeholder-shown)]:text-sm">
    Email
  </label>
</div>

// Checkbox animation
<label className="flex items-center gap-2 cursor-pointer">
  <div className="relative">
    <input type="checkbox" className="peer sr-only" />
    <div className="w-5 h-5 border-2 rounded transition-colors peer-checked:bg-blue-600 peer-checked:border-blue-600" />
    <CheckIcon className="absolute inset-0 m-auto w-3 h-3 text-white opacity-0 scale-0 transition-all peer-checked:opacity-100 peer-checked:scale-100" />
  </div>
  Label text
</label>

// Toggle switch
<button
  role="switch"
  aria-checked={enabled}
  onClick={() => setEnabled(!enabled)}
  className={cn(
    "relative w-11 h-6 rounded-full transition-colors",
    enabled ? "bg-blue-600" : "bg-gray-200"
  )}
>
  <span className={cn(
    "absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform",
    enabled && "translate-x-5"
  )} />
</button>
```

## Success/Error States

```tsx
// Success checkmark
<div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
  <svg className="w-8 h-8 text-green-600" viewBox="0 0 24 24">
    <path
      className="animate-[draw_0.5s_ease-out_forwards]"
      fill="none"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray="24"
      strokeDashoffset="24"
      d="M5 13l4 4L19 7"
    />
  </svg>
</div>

// Error shake
<input className="animate-[shake_0.5s_ease-in-out] border-red-500" />
```

```css
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```
