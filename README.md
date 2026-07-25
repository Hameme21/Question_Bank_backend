# UIU CSE Question Bank — Backend

The API server that powers the [UIU Question Bank](https://github.com/Hameme21/UIU_Question_Bank) frontend. It handles signed file uploads, Firebase-authenticated admin actions, and email notifications for student submissions.

**Live:** [`question-bank-x5pu.onrender.com`](https://question-bank-x5pu.onrender.com)
**Frontend:** [UIU CSE Question Bank](https://question-bank-orpin-psi.vercel.app/)

## What it does

- Signs Cloudinary uploads so the frontend can upload question papers, solutions, and notes directly and securely, without exposing API secrets
- Validates and shapes submission metadata (course code, topic, trimester, exam type, attached assets) before it's saved to Firestore from the client
- Verifies Firebase ID tokens and checks against an admin email allowlist for any privileged action (deleting or approving assets)
- Sends approval/rejection email notifications to students via SMTP (Nodemailer)
- Tracks lightweight live "active users" presence via a heartbeat endpoint
- Serves the frontend's static pages when run as a combined server

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/api/health` | Health check + config status |
| GET | `/api/cloudinary/config` | Public Cloudinary config (cloud name, folder) |
| POST | `/api/cloudinary/sign-upload` | Returns a signed payload for a direct-to-Cloudinary upload |
| POST | `/api/cloudinary/delete` | *(admin only)* Deletes a Cloudinary asset |
| POST | `/api/cloudinary/approve-assets` | *(admin only)* Tags assets as approved |
| POST | `/api/questions/submit` | Validates and normalizes a new question-bank submission |
| POST | `/api/questions/notify` | *(admin only)* Emails a submitter about approval/rejection |
| GET/POST | `/api/presence/heartbeat` | Tracks active viewer sessions |

Admin-only routes require an `Authorization: Bearer <Firebase ID token>` header, and the token's email must be in `ADMIN_EMAILS`.

## Tech Stack

- **Runtime:** Node.js (built-in `http` module — no framework)
- **Auth:** Firebase Identity Toolkit (token verification)
- **File storage:** Cloudinary (signed uploads, tagging, deletion)
- **Email:** Nodemailer over SMTP
- **Hosting:** Render

## Environment Variables

```env
PORT=4175
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_UPLOAD_FOLDER=uiu-toolkits/question-bank
FIREBASE_WEB_API_KEY=
ADMIN_EMAILS=admin1@uiu.ac.bd,admin2@uiu.ac.bd
ALLOWED_ORIGINS=*
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
EMAIL_FROM="UIU Toolkits <noreply@uiu-toolkits.com>"
```

## Getting Started

```bash
git clone https://github.com/Hameme21/Question_Bank_backend.git
cd Question_Bank_backend
npm install
# create a .env file with the variables above, or set them in your shell
npm start
```

The server starts on `http://localhost:4175` by default.

## Related Projects

- [UIU_Question_Bank](https://github.com/Hameme21/UIU_Question_Bank) — the student-facing frontend this API serves
- [QB_Admin](https://github.com/Hameme21/QB_Admin) — the admin portal for reviewing submissions
- [QB_admin_backend](https://github.com/Hameme21/QB_admin_backend) — the sibling backend for the admin portal

## License

Licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
