# SEO and Conversion Tracking

## Meta Tags

```tsx
// app/layout.tsx or pages/_app.tsx
export const metadata = {
  title: 'Product Name - Main Benefit | Brand',
  description: 'Clear description with keywords. 150-160 chars.',
  openGraph: {
    title: 'Product Name - Main Benefit',
    description: 'Description for social sharing',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
  },
};
```

## Structured Data

```tsx
<script type="application/ld+json">
  {JSON.stringify({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Product Name",
    "applicationCategory": "BusinessApplication",
    "offers": {
      "@type": "Offer",
      "price": "29",
      "priceCurrency": "USD"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "1250"
    }
  })}
</script>
```

## Conversion Tracking

```tsx
// Google Analytics 4 events
const trackCTA = (ctaName: string) => {
  gtag('event', 'cta_click', {
    cta_name: ctaName,
    page_location: window.location.href,
  });
};

// Track scroll depth
useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          gtag('event', 'section_viewed', {
            section_name: entry.target.id,
          });
        }
      });
    },
    { threshold: 0.5 }
  );

  document.querySelectorAll('section[id]').forEach((section) => {
    observer.observe(section);
  });
}, []);
```

## A/B Testing Elements

Priority elements to test:
1. **Headline copy** - Different value propositions
2. **CTA text** - "Start Free" vs "Get Started" vs "Try Now"
3. **CTA color** - High contrast options
4. **Hero image** - Product vs people vs abstract
5. **Social proof placement** - Above vs below fold
6. **Pricing display** - Monthly vs annual default
7. **Form length** - Email only vs full form
