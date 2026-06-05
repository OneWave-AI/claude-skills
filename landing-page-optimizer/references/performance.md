# Performance Optimization

## Image Optimization

```tsx
// Next.js Image component
import Image from 'next/image';

<Image
  src="/hero.png"
  alt="Product screenshot"
  width={1200}
  height={800}
  priority // Above-fold images
  placeholder="blur"
  blurDataURL={blurData}
/>

// Lazy load below-fold images
<Image
  src="/feature.png"
  loading="lazy"
  ...
/>
```

## Critical CSS

```tsx
// Inline critical styles for above-fold
<head>
  <style dangerouslySetInnerHTML={{ __html: criticalCSS }} />
  <link rel="preload" href="/fonts/inter.woff2" as="font" crossOrigin="" />
</head>
```

## Performance Targets

| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID/INP | < 100ms |
| CLS | < 0.1 |
| Total Size | < 1MB |
| Time to Interactive | < 3s |

## Mobile Optimization

```tsx
// Thumb-friendly CTAs
<Button className="w-full md:w-auto h-14 text-lg">
  Get Started
</Button>

// Sticky mobile CTA
<div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t md:hidden">
  <Button className="w-full">Start Free Trial</Button>
</div>

// Reduce content on mobile
<p className="hidden md:block">
  {fullDescription}
</p>
<p className="md:hidden">
  {shortDescription}
</p>
```
