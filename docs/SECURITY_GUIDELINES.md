# Security Guidelines

## Environment Variables
- Always use `os.getenv()` in code
- Never commit `.env` files
- Use `.env.example` for templates

## Production Checklist
- [ ] Rotate SECRET_KEY
- [ ] Restrict DB access
- [ ] Configure HTTPS
- [ ] Enable 2FA for admin
