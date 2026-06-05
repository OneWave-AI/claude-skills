# CSS Transitions

## Basic Syntax

```css
.element {
  /* Single property */
  transition: opacity 0.3s ease;

  /* Multiple properties */
  transition:
    transform 0.3s ease,
    opacity 0.3s ease,
    background-color 0.2s ease;

  /* Shorthand: property duration timing-function delay */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) 0s;
}
```

## Easing Functions

```css
/* Built-in */
transition-timing-function: linear;
transition-timing-function: ease;        /* Default - slow start, fast middle, slow end */
transition-timing-function: ease-in;     /* Slow start */
transition-timing-function: ease-out;    /* Slow end */
transition-timing-function: ease-in-out; /* Slow start and end */

/* Custom cubic-bezier */
/* Material Design standard */
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

/* Decelerate (entering) */
transition-timing-function: cubic-bezier(0, 0, 0.2, 1);

/* Accelerate (exiting) */
transition-timing-function: cubic-bezier(0.4, 0, 1, 1);

/* Bounce effect */
transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Elastic */
transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

## Tailwind Transitions

```tsx
// Duration
<div className="transition duration-150" />  // 150ms
<div className="transition duration-300" />  // 300ms
<div className="transition duration-500" />  // 500ms

// Timing function
<div className="transition ease-linear" />
<div className="transition ease-in" />
<div className="transition ease-out" />
<div className="transition ease-in-out" />

// Specific properties (better performance)
<div className="transition-opacity" />
<div className="transition-transform" />
<div className="transition-colors" />
<div className="transition-shadow" />
<div className="transition-all" />

// Combined
<button className="transition-all duration-200 ease-out hover:scale-105 hover:shadow-lg">
  Hover me
</button>
```
