# Loading Animations

## Spinners

```tsx
// Simple spinner
<div className="w-8 h-8 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin" />

// Dual ring
<div className="relative w-12 h-12">
  <div className="absolute inset-0 border-4 border-blue-200 rounded-full" />
  <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 rounded-full animate-spin" />
</div>

// Gradient spinner
<div className="w-10 h-10 rounded-full animate-spin"
  style={{
    background: 'conic-gradient(from 0deg, transparent, #3b82f6)',
    mask: 'radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 3px))'
  }}
/>
```

```css
/* Pulsing ring */
@keyframes pingRing {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.ping-ring {
  position: relative;
}

.ping-ring::before {
  content: '';
  position: absolute;
  inset: 0;
  border: 2px solid currentColor;
  border-radius: 50%;
  animation: pingRing 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}
```

## Dots Loading

```tsx
// Bouncing dots
<div className="flex gap-1">
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]" />
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]" />
  <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" />
</div>

// Pulsing dots
<div className="flex gap-1">
  {[0, 1, 2].map((i) => (
    <div
      key={i}
      className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"
      style={{ animationDelay: `${i * 0.15}s` }}
    />
  ))}
</div>
```

```css
/* Scaling dots */
@keyframes dotScale {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.dot-loader {
  display: flex;
  gap: 4px;
}

.dot-loader span {
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  animation: dotScale 1.4s ease-in-out infinite;
}

.dot-loader span:nth-child(1) { animation-delay: -0.32s; }
.dot-loader span:nth-child(2) { animation-delay: -0.16s; }
.dot-loader span:nth-child(3) { animation-delay: 0s; }
```

## Skeleton Loaders

```tsx
// Basic skeleton
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
  <div className="h-4 bg-gray-200 rounded w-5/6" />
</div>

// Card skeleton
<div className="animate-pulse">
  <div className="bg-gray-200 h-48 rounded-t-lg" />
  <div className="p-4 space-y-3">
    <div className="h-4 bg-gray-200 rounded w-3/4" />
    <div className="h-4 bg-gray-200 rounded w-1/2" />
  </div>
</div>

// Shimmer effect
<div className="relative overflow-hidden bg-gray-200 rounded">
  <div className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/60 to-transparent" />
</div>
```

```css
/* Shimmer keyframe */
@keyframes shimmer {
  100% { transform: translateX(100%); }
}
```

## Progress Bars

```tsx
// Indeterminate progress
<div className="h-1 w-full bg-gray-200 rounded overflow-hidden">
  <div className="h-full bg-blue-600 w-1/3 animate-[progress_1s_ease-in-out_infinite]" />
</div>

// Striped progress
<div className="h-2 w-full bg-gray-200 rounded overflow-hidden">
  <div
    className="h-full bg-blue-600 transition-all duration-300"
    style={{
      width: `${progress}%`,
      backgroundImage: 'linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%)',
      backgroundSize: '1rem 1rem',
      animation: 'progress-stripes 1s linear infinite'
    }}
  />
</div>
```

```css
@keyframes progress {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}

@keyframes progress-stripes {
  from { background-position: 1rem 0; }
  to { background-position: 0 0; }
}
```
