# Production Deployment Checklist

## Pre-Deployment Checks

### Backend (Railway/Vercel/Render)
- [ ] **Environment Variables**: All required environment variables are set
- [ ] **Database Connection**: Neon database connection established
- [ ] **Vector Store**: Qdrant connection established
- [ ] **API Keys**: OpenAI and other API keys configured
- [ ] **Security**: CORS settings restricted to production domain
- [ ] **Rate Limiting**: Proper limits configured for production traffic
- [ ] **Logging**: Production logging levels set
- [ ] **Health Checks**: `/health` endpoint responds correctly
- [ ] **SSL/TLS**: SSL certificate configured

### Frontend (GitHub Pages)
- [ ] **Base URL**: Base URL configured correctly in docusaurus.config.ts
- [ ] **API Endpoint**: Backend API endpoint updated to production URL
- [ ] **Analytics**: Google Analytics or other analytics configured (optional)
- [ ] **Build**: `npm run build` completes successfully
- [ ] **Static Assets**: All assets properly loaded in production build
- [ ] **SEO**: Meta tags and SEO settings configured

## Deployment Steps

### Backend Deployment
1. **Push to Repository**: Push code to main branch
2. **Deploy to Platform**:
   - For Railway: Link repository and deploy
   - For Render: Connect repository and configure
   - For Vercel: Connect repository and configure
3. **Configure Environment Variables**:
   ```
   NEON_DATABASE_URL=your_neon_db_url
   QDRANT_URL=your_qdrant_url
   OPENAI_API_KEY=your_openai_key
   SECRET_KEY=your_production_secret
   ```
4. **Verify Deployment**: Check logs and health endpoint

### Frontend Deployment
1. **Update API Endpoint**: Change backend API URL in frontend to production
2. **Build**: Run `npm run build`
3. **Deploy to GitHub Pages**:
   - Run `GIT_USER=<your-username> DEPLOYMENT_BRANCH=gh-pages npm run deploy`
   - Or use GitHub Actions workflow

## Post-Deployment Verification

### Backend Verification
- [ ] **Health Check**: `GET /health` returns healthy status
- [ ] **API Documentation**: `/docs` accessible (temporarily)
- [ ] **Endpoints**: All API endpoints return 200 for valid requests
- [ ] **Database**: Database operations work correctly
- [ ] **External APIs**: OpenAI and other external APIs accessible
- [ ] **Rate Limiting**: Rate limits working as expected
- [ ] **Caching**: Cache functionality working

### Frontend Verification
- [ ] **Homepage**: Loads without errors
- [ ] **Navigation**: All navigation links work
- [ ] **Chat Widget**: AI chat widget connects to backend
- [ ] **Text Selection**: Text selection functionality works
- [ ] **Mobile**: Responsive design works on mobile devices
- [ ] **Performance**: Page load times acceptable (< 3 seconds)

## Rollback Plan
- [ ] **Backend Rollback**: Keep previous version running during deployment
- [ ] **Frontend Rollback**: Maintain previous build in case of issues
- [ ] **Database Migrations**: Have rollback scripts ready if needed

## Monitoring
- [ ] **Error Tracking**: Set up error tracking (Sentry, etc.)
- [ ] **Performance Monitoring**: Set up performance monitoring
- [ ] **Log Monitoring**: Set up log monitoring and alerts
- [ ] **Uptime Monitoring**: Set up uptime monitoring

## Launch Checklist
- [ ] **Final Testing**: End-to-end testing completed
- [ ] **Performance Testing**: Load testing completed (if needed)
- [ ] **Security Scanning**: Security scan completed
- [ ] **Documentation**: Deployment documentation updated
- [ ] **Team Notification**: Team notified of deployment
- [ ] **Go Live**: Announce launch and monitor

## Emergency Contacts
- Backend deployment contact: [contact info]
- Frontend deployment contact: [contact info]
- Infrastructure contact: [contact info]

## Known Issues
- Python 3.13 compatibility issue with SQLAlchemy (resolved by using Python 3.11 in deployment)