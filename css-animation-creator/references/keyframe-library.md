# Keyframe Animations

## Basic Syntax

```css
@keyframes animationName {
  0% { /* starting state */ }
  50% { /* midpoint state */ }
  100% { /* ending state */ }
}

.element {
  animation: animationName 1s ease-in-out infinite;
  /* name | duration | timing | iteration-count */

  /* Full syntax */
  animation-name: animationName;
  animation-duration: 1s;
  animation-timing-function: ease-in-out;
  animation-delay: 0s;
  animation-iteration-count: infinite; /* or number */
  animation-direction: normal; /* reverse, alternate, alternate-reverse */
  animation-fill-mode: forwards; /* none, forwards, backwards, both */
  animation-play-state: running; /* paused */
}
```

## Fade Animations

```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Fade In Up */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Down */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Left */
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Fade In Right */
@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Fade In Scale */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Fade Out */
@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}
```

## Scale Animations

```css
/* Scale In */
@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

/* Scale In Bounce */
@keyframes scaleInBounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Pop */
@keyframes pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Heartbeat */
@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  14% { transform: scale(1.3); }
  28% { transform: scale(1); }
  42% { transform: scale(1.3); }
  70% { transform: scale(1); }
}
```

## Bounce Animations

```css
/* Bounce */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
}

/* Bounce In */
@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

/* Bounce In Down */
@keyframes bounceInDown {
  0% {
    opacity: 0;
    transform: translateY(-100px);
  }
  60% {
    opacity: 1;
    transform: translateY(20px);
  }
  80% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

/* Rubber Band */
@keyframes rubberBand {
  0% { transform: scaleX(1); }
  30% { transform: scaleX(1.25) scaleY(0.75); }
  40% { transform: scaleX(0.75) scaleY(1.25); }
  50% { transform: scaleX(1.15) scaleY(0.85); }
  65% { transform: scaleX(0.95) scaleY(1.05); }
  75% { transform: scaleX(1.05) scaleY(0.95); }
  100% { transform: scaleX(1) scaleY(1); }
}
```

## Rotate Animations

```css
/* Spin */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Spin Reverse */
@keyframes spinReverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

/* Swing */
@keyframes swing {
  20% { transform: rotate(15deg); }
  40% { transform: rotate(-10deg); }
  60% { transform: rotate(5deg); }
  80% { transform: rotate(-5deg); }
  100% { transform: rotate(0deg); }
}

/* Wobble */
@keyframes wobble {
  0% { transform: translateX(0); }
  15% { transform: translateX(-15px) rotate(-5deg); }
  30% { transform: translateX(12px) rotate(3deg); }
  45% { transform: translateX(-9px) rotate(-3deg); }
  60% { transform: translateX(6px) rotate(2deg); }
  75% { transform: translateX(-3px) rotate(-1deg); }
  100% { transform: translateX(0); }
}

/* Flip */
@keyframes flipX {
  0% { transform: perspective(400px) rotateX(90deg); opacity: 0; }
  40% { transform: perspective(400px) rotateX(-20deg); }
  60% { transform: perspective(400px) rotateX(10deg); opacity: 1; }
  80% { transform: perspective(400px) rotateX(-5deg); }
  100% { transform: perspective(400px) rotateX(0deg); }
}
```

## Slide Animations

```css
/* Slide In Up */
@keyframes slideInUp {
  from {
    transform: translateY(100%);
    visibility: visible;
  }
  to { transform: translateY(0); }
}

/* Slide In Down */
@keyframes slideInDown {
  from {
    transform: translateY(-100%);
    visibility: visible;
  }
  to { transform: translateY(0); }
}

/* Slide In Left */
@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
    visibility: visible;
  }
  to { transform: translateX(0); }
}

/* Slide In Right */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    visibility: visible;
  }
  to { transform: translateX(0); }
}

/* Slide Out */
@keyframes slideOutUp {
  from { transform: translateY(0); }
  to {
    transform: translateY(-100%);
    visibility: hidden;
  }
}
```

## Attention Seekers

```css
/* Shake */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

/* Shake Horizontal (stronger) */
@keyframes shakeX {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
  20%, 40%, 60%, 80% { transform: translateX(10px); }
}

/* Jello */
@keyframes jello {
  0%, 11.1%, 100% { transform: none; }
  22.2% { transform: skewX(-12.5deg) skewY(-12.5deg); }
  33.3% { transform: skewX(6.25deg) skewY(6.25deg); }
  44.4% { transform: skewX(-3.125deg) skewY(-3.125deg); }
  55.5% { transform: skewX(1.5625deg) skewY(1.5625deg); }
  66.6% { transform: skewX(-0.78125deg) skewY(-0.78125deg); }
  77.7% { transform: skewX(0.390625deg) skewY(0.390625deg); }
  88.8% { transform: skewX(-0.1953125deg) skewY(-0.1953125deg); }
}

/* Flash */
@keyframes flash {
  0%, 50%, 100% { opacity: 1; }
  25%, 75% { opacity: 0; }
}

/* Tada */
@keyframes tada {
  0% { transform: scale(1) rotate(0); }
  10%, 20% { transform: scale(0.9) rotate(-3deg); }
  30%, 50%, 70%, 90% { transform: scale(1.1) rotate(3deg); }
  40%, 60%, 80% { transform: scale(1.1) rotate(-3deg); }
  100% { transform: scale(1) rotate(0); }
}
```
