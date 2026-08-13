# Aquashield — User / Complaint Module (Frontend)

Simple static frontend demo for citizen complaint flows. No backend included — data is stored in `localStorage` for demo purposes.

Try it:

1. Open `index.html` in a browser.
2. Sign up at `signup.html`.
3. Register complaints at `complaint.html` (images are stored as Base64 in `localStorage`).
4. View your complaints and statuses at `profile.html`.

Notes:
- This is a starting point for integrating with an API. Replace localStorage calls with fetch/XHR to a server.
- Images are encoded inline; for production, upload to a server or object store.
