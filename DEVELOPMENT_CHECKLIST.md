# 🔧 Development Checklist - Audio to MIDI Backend

**Created by Sergie Code**

## ✅ Pre-Development Setup

### Environment Setup
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Environment activated (`.\venv\Scripts\activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] All tests passing (`python -m pytest tests/ -v`)

### Project Structure Verification
- [ ] `src/` directory with transcription module
- [ ] `tests/` directory with comprehensive tests
- [ ] `uploads/` and `output/` directories created
- [ ] All configuration files present

## 🧪 Testing Checklist

### Before Making Changes
- [ ] Run full test suite: `python -m pytest tests/ -v`
- [ ] Check health endpoint: http://localhost:5000/health
- [ ] Verify server starts without errors: `python app.py`

### After Making Changes
- [ ] Re-run all tests
- [ ] Test affected API endpoints manually
- [ ] Check for new errors in terminal output
- [ ] Verify MIDI file generation still works

## 🔄 Development Workflow

### Adding New Features
1. [ ] Write tests first (TDD approach)
2. [ ] Implement feature in appropriate module
3. [ ] Update API endpoints if needed
4. [ ] Run tests to ensure nothing breaks
5. [ ] Update documentation

### API Endpoint Changes
1. [ ] Update `app.py` with new routes
2. [ ] Add corresponding tests in `tests/test_api.py`
3. [ ] Update example usage scripts
4. [ ] Test with Postman or curl

### ML Model Integration
1. [ ] Update `src/transcription/transcriber.py`
2. [ ] Add model dependencies to `requirements.txt`
3. [ ] Create model-specific tests
4. [ ] Update configuration for model paths

## 🐛 Debugging Guide

### Common Issues and Solutions

#### Server Won't Start
- [ ] Check if port 5000 is already in use
- [ ] Verify virtual environment is activated
- [ ] Check for missing dependencies
- [ ] Look for syntax errors in recent changes

#### Tests Failing
- [ ] Check if server is running (stop it for tests)
- [ ] Verify all dependencies are installed
- [ ] Check for file permission issues on Windows
- [ ] Look at specific test failure messages

#### Import Errors
- [ ] Ensure `src` directory has `__init__.py` files
- [ ] Check Python path configuration
- [ ] Verify virtual environment activation
- [ ] Reinstall problematic packages

#### MIDI Generation Issues
- [ ] Check `pretty_midi` installation
- [ ] Verify audio file format support
- [ ] Test with known good audio files
- [ ] Check file permissions in output directory

## 📝 Code Quality Checklist

### Before Committing
- [ ] All tests pass
- [ ] No syntax errors or warnings
- [ ] Code follows Python PEP 8 style
- [ ] Docstrings added for new functions
- [ ] Error handling implemented

### Code Review Points
- [ ] Secure file handling (no path traversal)
- [ ] Proper error messages for users
- [ ] Logging for debugging
- [ ] Input validation
- [ ] Resource cleanup (temp files)

## 🚀 Deployment Preparation

### Production Readiness
- [ ] Change Flask debug mode to False
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up proper logging
- [ ] Configure environment variables
- [ ] Test with production-like data volumes

### Security Review
- [ ] File upload size limits configured
- [ ] File type validation in place
- [ ] No sensitive data in logs
- [ ] CORS configured if needed
- [ ] Rate limiting considered

## 📚 Documentation Maintenance

### Keep Updated
- [ ] README.md with latest setup instructions
- [ ] API documentation with new endpoints
- [ ] Example usage scripts working
- [ ] Requirements.txt with exact versions
- [ ] Test report with current status

## 🎥 YouTube Content Preparation

### Demo Readiness
- [ ] Server starts cleanly
- [ ] All endpoints respond correctly
- [ ] Example files ready for demo
- [ ] Error scenarios prepared
- [ ] Performance considerations noted

### Tutorial Preparation
- [ ] Clean project state
- [ ] Step-by-step setup verified
- [ ] Common issues documented
- [ ] Extension points identified
- [ ] Next steps outlined

## 🔧 Maintenance Tasks

### Weekly
- [ ] Run full test suite
- [ ] Check for dependency updates
- [ ] Review error logs
- [ ] Test with different audio files

### Monthly
- [ ] Update dependencies (carefully)
- [ ] Review security best practices
- [ ] Check for code optimization opportunities
- [ ] Update documentation

### Before Major Changes
- [ ] Create backup/branch
- [ ] Document current working state
- [ ] Plan rollback strategy
- [ ] Test in isolated environment

---

## 🆘 Emergency Fixes

### If Everything Breaks
1. **Revert to last known good state**
   ```bash
   git checkout [last-good-commit]
   ```

2. **Clean reinstall**
   ```bash
   rm -rf venv
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Test basic functionality**
   ```bash
   python -m pytest tests/test_api.py::test_health_endpoint -v
   ```

### Quick Health Check
```bash
# All these should work:
python app.py &
curl http://localhost:5000/health
python simple_test.py
python -m pytest tests/ -v
```

---

**Remember**: When in doubt, run the tests! 🧪  
**Created by Sergie Code - AI Tools for Musicians**
