# TimeTwin — AI Watch Discovery Platform

Build a modern full-stack web application called “Wynd”.

## Product Concept

Wynd is an AI-powered watch discovery platform where users can:

* Upload a watch image
* Find visually similar watches
* Get cheaper alternatives
* Receive personalized recommendations
* Save collections
* Swipe through watches TikTok/Tinder style

The app should feel premium, modern, and startup-quality.

---

# Tech Stack

## Frontend

* Next.js 15
* TypeScript
* TailwindCSS
* Framer Motion
* shadcn/ui

## Backend

* FastAPI (Python)

## Database

* PostgreSQL

## AI / Search

* CLIP embeddings for image similarity
* pgvector for vector search

## Authentication

* Clerk or NextAuth

## Deployment

* Vercel frontend
* Railway or Render backend

---

# Design Requirements

The UI should feel like:

* luxury
* minimal
* smooth
* mobile-first

Use:

* black
* white
* silver
* subtle animations
* large imagery
* rounded cards
* glassmorphism sparingly

Avoid:

* clutter
* bright colors
* generic dashboard appearance

The homepage should immediately communicate:
“Find watches that match your style.”

---

# Core Features

## 1. AI Image Search

Users can upload an image of a watch.

The system should:

* analyze the image
* generate embeddings
* compare against stored watch embeddings
* return visually similar watches

Results should include:

* image
* brand
* model
* estimated price
* similarity score

---

## 2. Budget Alternatives

Users can set a max budget.

Example:
“Show watches like this under $300.”

The backend should:

* filter recommendations by price
* preserve visual similarity ranking

---

## 3. Personalized Recommendation Engine

Users can:

* like watches
* save watches
* skip watches

The system should learn preferences based on:

* case shape
* dial color
* strap type
* brand style
* price range

Implement a recommendation pipeline that improves over time.

---

## 4. Swipe Discovery Feed

Build a vertical swipe interface similar to TikTok.

Each card should show:

* watch image
* model
* price
* quick actions:

  * like
  * save
  * view similar

Smooth animations are critical.

---

## 5. Collections

Users can:

* save favorite watches
* organize collections
* create wishlists

---

# Database Schema

Create models for:

* users
* watches
* embeddings
* likes
* saved_collections
* user_preferences

The watches table should include:

* id
* brand
* model
* image_url
* price
* style_tags
* embedding vector

---

# AI Requirements

Use OpenAI CLIP embeddings or equivalent vision embeddings.

Implement:

* cosine similarity search
* nearest-neighbor retrieval
* vector indexing with pgvector

The app should support fast similarity search.

---

# API Endpoints

Implement:

* image upload
* recommendation retrieval
* similar watch search
* save/like watch
* user profile
* collections

Use clean REST architecture.

---

# Frontend Pages

Create:

* landing page
* discover page
* upload page
* collections page
* profile page
* watch detail page

---

# Landing Page Requirements

Hero section:
“Upload any watch. Find your TimeTwin.”

Include:

* animated demo
* featured watches
* trending styles
* CTA buttons

---

# Important Engineering Requirements

* Use clean architecture
* Use reusable components
* Use proper TypeScript typing
* Use loading skeletons
* Add error handling
* Optimize image loading
* Use server-side rendering where appropriate
* Make everything responsive

---

# Stretch Features

If time permits:

* celebrity watch matching
* price prediction trends
* social feed
* comments
* follow users
* AI-generated style explanations

Example:
“You seem to prefer minimalist integrated-bracelet sports watches.”

---

# Deliverables

Generate:

1. full project structure
2. database schema
3. backend API implementation
4. frontend pages/components
5. embedding pipeline
6. vector similarity search
7. authentication flow
8. responsive UI
9. README with setup instructions

The final product should look like a real funded startup MVP.
