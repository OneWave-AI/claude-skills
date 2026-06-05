# Page Structure Template

Optimal eight-section landing page layout (React/Tailwind).

```tsx
// Optimal landing page structure
<main>
  {/* 1. Hero Section */}
  <section className="min-h-[80vh] flex items-center">
    <div className="max-w-6xl mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <Badge>New Feature</Badge>
        <h1 className="text-4xl lg:text-6xl font-bold mt-4">
          Main Value Proposition
        </h1>
        <p className="text-xl text-gray-600 mt-6">
          Supporting statement that expands on the benefit
        </p>
        <div className="flex gap-4 mt-8">
          <Button size="lg">Primary CTA</Button>
          <Button size="lg" variant="outline">Secondary CTA</Button>
        </div>
        <div className="flex items-center gap-6 mt-8">
          <div className="flex -space-x-2">
            {avatars.map(a => <Avatar key={a.id} src={a.src} />)}
          </div>
          <p className="text-sm text-gray-600">
            <strong>2,000+</strong> happy customers
          </p>
        </div>
      </div>
      <div>
        <img src="/hero-image.png" alt="Product preview" />
      </div>
    </div>
  </section>

  {/* 2. Social Proof - Logos */}
  <section className="py-12 bg-gray-50">
    <p className="text-center text-gray-500 mb-8">Trusted by leading companies</p>
    <div className="flex justify-center gap-12 opacity-60">
      {logos.map(logo => <img key={logo.name} src={logo.src} alt={logo.name} />)}
    </div>
  </section>

  {/* 3. Problem/Solution */}
  <section className="py-20">
    <div className="max-w-3xl mx-auto text-center">
      <h2 className="text-3xl font-bold">The Problem</h2>
      <p className="text-xl text-gray-600 mt-4">
        Describe the pain point your audience faces
      </p>
    </div>
  </section>

  {/* 4. Features/Benefits */}
  <section className="py-20 bg-gray-50">
    <h2 className="text-3xl font-bold text-center">How It Works</h2>
    <div className="grid md:grid-cols-3 gap-8 mt-12 max-w-6xl mx-auto">
      {features.map(feature => (
        <Card key={feature.title}>
          <feature.icon className="w-12 h-12 text-primary-500" />
          <h3 className="text-xl font-semibold mt-4">{feature.title}</h3>
          <p className="text-gray-600 mt-2">{feature.description}</p>
        </Card>
      ))}
    </div>
  </section>

  {/* 5. Testimonials */}
  <section className="py-20">
    <h2 className="text-3xl font-bold text-center">What Customers Say</h2>
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
      {testimonials.map(t => (
        <TestimonialCard key={t.name} {...t} />
      ))}
    </div>
  </section>

  {/* 6. Pricing (if applicable) */}
  <section className="py-20 bg-gray-50">
    <PricingTable plans={plans} />
  </section>

  {/* 7. FAQ */}
  <section className="py-20">
    <h2 className="text-3xl font-bold text-center">FAQ</h2>
    <Accordion items={faqs} className="max-w-3xl mx-auto mt-12" />
  </section>

  {/* 8. Final CTA */}
  <section className="py-20 bg-primary-600 text-white text-center">
    <h2 className="text-3xl font-bold">Ready to Get Started?</h2>
    <p className="text-xl opacity-90 mt-4">Join 2,000+ companies already using our product</p>
    <Button size="lg" variant="secondary" className="mt-8">
      Start Free Trial
    </Button>
    <p className="text-sm opacity-75 mt-4">No credit card required</p>
  </section>
</main>
```
