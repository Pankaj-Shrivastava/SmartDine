---
name: Premium AI Dining Intelligence
colors:
  surface: '#1d1011'
  surface-dim: '#1d1011'
  surface-bright: '#463536'
  surface-container-lowest: '#170b0c'
  surface-container-low: '#261819'
  surface-container: '#2b1c1d'
  surface-container-high: '#362627'
  surface-container-highest: '#413031'
  on-surface: '#f7dcdd'
  on-surface-variant: '#e2bebf'
  inverse-surface: '#f7dcdd'
  inverse-on-surface: '#3d2c2d'
  outline: '#a9898a'
  outline-variant: '#5a4042'
  surface-tint: '#ffb2b7'
  primary: '#ffb2b7'
  on-primary: '#67001c'
  primary-container: '#fc536d'
  on-primary-container: '#5b0017'
  inverse-primary: '#b71d3f'
  secondary: '#a4c9ff'
  on-secondary: '#00315d'
  secondary-container: '#3b93f3'
  on-secondary-container: '#002a52'
  tertiary: '#66dd8b'
  on-tertiary: '#003919'
  tertiary-container: '#25a55a'
  on-tertiary-container: '#003115'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdadb'
  primary-fixed-dim: '#ffb2b7'
  on-primary-fixed: '#40000e'
  on-primary-fixed-variant: '#91002b'
  secondary-fixed: '#d4e3ff'
  secondary-fixed-dim: '#a4c9ff'
  on-secondary-fixed: '#001c39'
  on-secondary-fixed-variant: '#004884'
  tertiary-fixed: '#83fba5'
  tertiary-fixed-dim: '#66dd8b'
  on-tertiary-fixed: '#00210c'
  on-tertiary-fixed-variant: '#005227'
  background: '#1d1011'
  on-background: '#f7dcdd'
  surface-variant: '#413031'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '300'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
---

## Brand & Style
The design system is engineered for a high-end, AI-powered gastronomic experience. It targets a discerning audience that values efficiency, precision, and a "white-glove" digital feel.

The aesthetic is **Modern Glassmorphism** layered over a **Minimalist Enterprise** foundation. By combining the deep, immersive void of space-navy with translucent, frosted glass elements, the UI evokes a sense of depth and technological sophistication. Every interaction should feel like peering through a high-tech lens at the culinary world. The emotional response is one of trust, exclusivity, and discovery.

## Colors
This design system utilizes a dark-mode first palette to emphasize depth and premium quality.
- **Primary (Vibrant Coral):** Reserved for high-intent actions, AI-driven suggestions, and primary brand touchpoints.
- **Secondary (Electric Blue):** Dedicated to spatial information, location markers, and navigation.
- **Tertiary (Emerald Green):** Indicates value, budget tiers, and positive availability.
- **Accent (Gold):** Exclusively for high-tier ratings, awards, and the #1 ranked recommendation.
- **Surface Strategy:** Backgrounds utilize a subtle vertical gradient from the core navy to a slightly lighter slate. Surfaces are never fully opaque; they rely on alpha-transparency to maintain the glass effect.

## Typography
The system relies entirely on **Inter** to project a systematic, SaaS-inspired precision. 
- **Hierarchy:** Use tighter tracking (letter-spacing) on larger headlines to maintain a compact, premium look. 
- **Weights:** Use Light (300) for captions and secondary descriptions to increase the contrast against bold headlines.
- **Readability:** Body text should maintain a 150% line-height to ensure comfort when reading restaurant reviews or menus.

## Layout & Spacing
This design system uses a **12-column fluid grid** for desktop dashboards and a **4-column grid** for mobile devices. 
- **Gutters:** Standardized at 24px on desktop and 16px on mobile to ensure breathing room between glass cards.
- **Margins:** A generous 48px outer margin on desktop creates a "contained" feel, reminiscent of high-end software tools.
- **Rhythm:** All spacing must be a multiple of the 4px base unit. Vertical rhythm is driven by the `lg` (24px) unit for section spacing.

## Elevation & Depth
Depth is not communicated through traditional drop shadows but through **optical transparency and light refraction**.
- **Level 1 (Base):** Deep space navy gradient.
- **Level 2 (Cards/Modules):** Glassmorphism layer. Background blur of 12px with a 4% white fill. A 1px border with 8% white opacity acts as a "specular highlight" on the edge of the glass.
- **Level 3 (Modals/Popovers):** Increased background blur (24px) and a subtle outer glow using the primary coral color at 5% opacity to simulate light emitting from the AI interface.

## Shapes
The shape language is sophisticated and approachable, avoiding the harshness of sharp corners while steering clear of overly bubbly aesthetics.
- **Cards:** Use a 16px radius to feel substantial and modern.
- **Controls:** Inputs use a slightly tighter 12px radius to differentiate functional elements from container elements.
- **Meta-data:** Chips and pills use an 8px radius, creating a distinct "tag" look that fits cleanly within cards.

## Components
- **Buttons:** Primary buttons use a solid Coral gradient with a soft outer glow of the same color. Secondary buttons use the "ghost glass" style with white-gray text.
- **Cards:** Every card must include the 1px interior border to define its shape against the dark background. Images inside cards should have a subtle inner-shadow to blend into the glass container.
- **Inputs:** Fields are dark-filled (rgba(0,0,0,0.2)) with a 1px border. On focus, the border transitions to Electric Blue with a subtle 4px outer blur.
- **Chips:** Used for cuisine types or price points. These should be semi-transparent with a 1px border matching the text color (e.g., Emerald for budget).
- **Location Markers:** Pulse animation using the Electric Blue color to indicate "Live AI Tracking."
- **Rating Stars:** Use the Gold accent color. For Rank 1 restaurants, the entire card gets a thin Gold top-border.