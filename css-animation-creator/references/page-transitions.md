# Page Transitions

## CSS-only Transitions

```css
/* View Transitions API (Chrome 111+) */
@view-transition {
  navigation: auto;
}

::view-transition-old(root) {
  animation: fadeOut 0.3s ease-out;
}

::view-transition-new(root) {
  animation: fadeIn 0.3s ease-in;
}

/* Specific element transitions */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 0.5s;
}
```

## Framer Motion

```tsx
import { motion, AnimatePresence } from 'framer-motion';

// Fade transition
const pageVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

function PageWrapper({ children }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        variants={pageVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

// Slide transition
const slideVariants = {
  initial: { opacity: 0, x: 20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -20 },
};

// Scale + fade
const scaleVariants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 1.05 },
};

// Shared layout animations
function Gallery({ items, selectedId }) {
  return (
    <>
      {items.map(item => (
        <motion.div key={item.id} layoutId={item.id}>
          <img src={item.src} />
        </motion.div>
      ))}

      <AnimatePresence>
        {selectedId && (
          <motion.div layoutId={selectedId} className="modal">
            <img src={items.find(i => i.id === selectedId).src} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

## Staggered Animations

```tsx
// Framer Motion stagger
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

function StaggeredList({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}

// CSS stagger with custom properties
<ul className="stagger-list">
  {items.map((item, i) => (
    <li
      key={item.id}
      style={{ '--i': i } as React.CSSProperties}
      className="animate-fadeInUp opacity-0"
    >
      {item.name}
    </li>
  ))}
</ul>
```

```css
.stagger-list li {
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: calc(var(--i) * 0.1s);
}
```
