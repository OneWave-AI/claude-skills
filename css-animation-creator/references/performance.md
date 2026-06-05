# Performance Best Practices

## GPU-Accelerated Properties

```css
/* GOOD - GPU accelerated */
transform: translateX(100px);
transform: scale(1.1);
transform: rotate(45deg);
opacity: 0.5;

/* BAD - Triggers layout/paint */
left: 100px;
top: 50px;
width: 200px;
height: 100px;
margin: 20px;
padding: 10px;
border-width: 2px;
font-size: 16px;
```

## will-change (Use Sparingly)

```css
/* Only when needed for complex animations */
.complex-animation {
  will-change: transform, opacity;
}

/* Remove after animation */
.complex-animation.done {
  will-change: auto;
}
```

## Contain for Isolation

```css
.animated-section {
  contain: layout style paint;
}
```

## Animation Performance Checklist

- [ ] Only animate `transform` and `opacity`
- [ ] Use `will-change` only when necessary
- [ ] Keep animations under 300ms for UI feedback
- [ ] Test on low-end devices
- [ ] Use `contain` for isolated sections
- [ ] Reduce animation during scroll
- [ ] Pause off-screen animations
