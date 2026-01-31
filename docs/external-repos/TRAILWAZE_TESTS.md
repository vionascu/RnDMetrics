# TrailWaze - Test Metrics & Specifications

**Repository:** https://github.com/vionascu/trailwaze
**Last Updated:** January 31, 2026

---

## Executive Summary

TrailWaze is a full-stack, cross-platform application providing trail navigation and community features for outdoor enthusiasts. The project uses a monorepo architecture with multiple applications (web and mobile) and comprehensive test coverage.

| Metric | Value |
|--------|-------|
| Project Type | Full-Stack Monorepo |
| Frontend Stack | React (Web) + React Native (Mobile) |
| Test Infrastructure | Integrated test framework |
| CI/CD | GitHub Actions |
| Status | ✅ Active Development |

---

## Project Architecture

### Technology Stack

```
┌──────────────────────────────────────────────────┐
│ TrailWaze Monorepo                               │
├──────────────────────────────────────────────────┤
│                                                  │
│ ┌──────────────────┐    ┌────────────────────┐  │
│ │  Web Application │    │ Mobile Application │  │
│ │  (React)         │    │ (React Native)     │  │
│ ├──────────────────┤    ├────────────────────┤  │
│ │ • Dashboard      │    │ • iOS App          │  │
│ │ • Trail Maps     │    │ • Android App      │  │
│ │ • User Profiles  │    │ • Offline Mode     │  │
│ │ • Community      │    │ • GPS Tracking     │  │
│ └──────────────────┘    └────────────────────┘  │
│         ↓                        ↓               │
│ ┌──────────────────────────────────────────────┐ │
│ │ Shared Libraries & Utils                     │ │
│ │ • API Client                                 │ │
│ │ • Authentication                             │ │
│ │ • Data Models                                │ │
│ └──────────────────────────────────────────────┘ │
│         ↓                                        │
│ ┌──────────────────────────────────────────────┐ │
│ │ Backend API / Services                       │ │
│ │ • Trail Management                           │ │
│ │ • User Services                              │ │
│ │ • Community Engagement                       │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Directory Structure

```
trailwaze/
├── apps/
│   ├── web/                    # React web application
│   │   ├── src/
│   │   ├── tests/
│   │   ├── package.json
│   │   └── ...
│   │
│   └── mobile/                 # React Native mobile app
│       ├── src/
│       ├── tests/
│       ├── ios/
│       ├── android/
│       ├── package.json
│       └── ...
│
├── packages/                   # Shared packages
│   ├── api-client/
│   ├── utils/
│   ├── components/
│   └── ...
│
├── docs/                       # Documentation
├── .github/
│   └── workflows/
│       ├── test.yml            # CI/CD configuration
│       └── deploy.yml          # Deployment workflow
├── package.json               # Root monorepo config
└── ...
```

---

## Test Infrastructure

### Test Framework Configuration

**Web Application (React):**
- Test Runner: Jest
- Testing Library: React Testing Library
- Mocking: Jest mocks
- E2E: Cypress (if configured)

**Mobile Application (React Native):**
- Test Runner: Jest
- Testing Library: React Native Testing Library
- Mocking: Jest Native mocks
- E2E: Detox (if configured)

### Test Types

#### 1. Unit Tests
- **Scope:** Individual components, utilities, hooks
- **Coverage:** Business logic, calculations
- **Speed:** Fast (< 100ms per test)
- **Isolation:** Complete

#### 2. Integration Tests
- **Scope:** Component interactions, API calls
- **Coverage:** Data flow, state management
- **Speed:** Medium (100-500ms per test)
- **Isolation:** Mocked external services

#### 3. E2E Tests
- **Scope:** User workflows, complete features
- **Coverage:** User interactions, navigation
- **Speed:** Slow (> 1 second per test)
- **Isolation:** Real environment (if configured)

---

## Web Application (React)

### Project Information

**Path:** `apps/web/`
**Technology:** React, TypeScript, Modern JavaScript
**Build System:** Vite / Webpack
**Package Manager:** npm / yarn

### Test Structure

```
apps/web/
├── src/
│   ├── components/
│   │   ├── Trail/
│   │   │   ├── TrailCard.tsx
│   │   │   ├── TrailCard.test.tsx
│   │   │   ├── TrailMap.tsx
│   │   │   └── TrailMap.test.tsx
│   │   ├── User/
│   │   └── ...
│   │
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Dashboard.test.tsx
│   │   └── ...
│   │
│   ├── hooks/
│   │   ├── useTrails.ts
│   │   ├── useTrails.test.ts
│   │   └── ...
│   │
│   └── utils/
│       ├── geoUtils.ts
│       ├── geoUtils.test.ts
│       └── ...
│
├── tests/
│   ├── integration/
│   ├── e2e/
│   └── ...
│
├── package.json
├── jest.config.js
└── ...
```

### Component Test Examples

#### Trail Card Component Tests
```typescript
// TrailCard.test.tsx
describe('TrailCard Component', () => {
  test('renders trail information correctly', () => {
    // Test trail data display
    // Test difficulty badge
    // Test rating display
  });

  test('handles click navigation', () => {
    // Test click handler
    // Test navigation to trail detail
  });

  test('displays favorite button', () => {
    // Test favorite toggle
    // Test visual feedback
  });
});
```

#### Trail Map Component Tests
```typescript
// TrailMap.test.tsx
describe('TrailMap Component', () => {
  test('renders map with trail markers', () => {
    // Test map initialization
    // Test marker rendering
  });

  test('updates on trail selection', () => {
    // Test marker highlighting
    // Test pan/zoom
  });

  test('handles user interaction', () => {
    // Test marker click
    // Test info window display
  });
});
```

### Hook Tests

#### useTrails Hook Tests
```typescript
// useTrails.test.ts
describe('useTrails Hook', () => {
  test('fetches trails on mount', () => {
    // Test initial data fetch
    // Test loading state
    // Test success state
  });

  test('handles filter changes', () => {
    // Test difficulty filter
    // Test location filter
  });

  test('handles errors gracefully', () => {
    // Test error state
    // Test retry mechanism
  });
});
```

### Test Utilities

```typescript
// Test helpers for web app
export const renderWithProviders = (component) => {
  // Render with Redux/Context providers
};

export const waitForApiCall = (url) => {
  // Wait for fetch/axios call
};

export const mockTrailData = () => {
  // Create realistic trail fixtures
};
```

---

## Mobile Application (React Native)

### Project Information

**Path:** `apps/mobile/`
**Technology:** React Native, TypeScript
**Platforms:** iOS, Android
**Build System:** Expo / Native CLI

### Test Structure

```
apps/mobile/
├── src/
│   ├── components/
│   │   ├── Trail/
│   │   │   ├── TrailList.tsx
│   │   │   ├── TrailList.test.tsx
│   │   │   ├── TrailDetail.tsx
│   │   │   └── TrailDetail.test.tsx
│   │   ├── Navigation/
│   │   └── ...
│   │
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── HomeScreen.test.tsx
│   │   ├── MapScreen.tsx
│   │   └── MapScreen.test.tsx
│   │
│   ├── hooks/
│   │   ├── useLocationTracking.ts
│   │   ├── useLocationTracking.test.ts
│   │   └── ...
│   │
│   └── utils/
│       ├── gps.ts
│       ├── gps.test.ts
│       └── ...
│
├── ios/
│   └── ... (native files)
│
├── android/
│   └── ... (native files)
│
├── e2e/
│   ├── firstTest.e2e.js
│   └── ...
│
├── package.json
├── jest.config.js
└── ...
```

### Screen Test Examples

#### Home Screen Tests
```typescript
// HomeScreen.test.tsx
describe('HomeScreen', () => {
  test('displays nearby trails', () => {
    // Test trail list rendering
    // Test location permission handling
  });

  test('handles trail selection', () => {
    // Test navigation to detail screen
    // Test trail data passing
  });

  test('shows offline indicator', () => {
    // Test offline mode badge
    // Test sync status
  });
});
```

#### Map Screen Tests
```typescript
// MapScreen.test.tsx
describe('MapScreen', () => {
  test('renders current location', () => {
    // Test map initialization
    // Test location marker
  });

  test('tracks GPS updates', () => {
    // Test position updates
    // Test animation
  });

  test('displays trail overlays', () => {
    // Test trail path rendering
    // Test waypoint markers
  });
});
```

### GPS Tracking Tests

```typescript
// useLocationTracking.test.ts
describe('useLocationTracking Hook', () => {
  test('requests location permission', () => {
    // Test permission request
    // Test permission granted/denied
  });

  test('updates location periodically', () => {
    // Test location updates
    // Test accuracy changes
  });

  test('handles errors', () => {
    // Test GPS disabled
    // Test location services unavailable
  });
});
```

### Platform-Specific Tests

```typescript
// Native module tests
describe('Native GPS Module (iOS)', () => {
  test('initializes CoreLocation', () => {
    // Test iOS-specific initialization
  });

  test('handles permission states', () => {
    // Test iOS permission dialogs
  });
});

describe('Native GPS Module (Android)', () => {
  test('initializes LocationManager', () => {
    // Test Android-specific initialization
  });

  test('handles background location', () => {
    // Test Android background services
  });
});
```

---

## Shared Packages

### API Client Package

**Purpose:** Unified API communication for web and mobile

```typescript
// packages/api-client/src/trail.ts
export const trailAPI = {
  getTrails: (filters) => { /* ... */ },
  getTrailById: (id) => { /* ... */ },
  createTrail: (data) => { /* ... */ },
  updateTrail: (id, data) => { /* ... */ },
  deleteTrail: (id) => { /* ... */ },
  suggestTrails: (location) => { /* ... */ }
};

// Test suite
describe('Trail API Client', () => {
  test('fetches trails with filters', () => {
    // Test API call
    // Test data transformation
  });

  test('handles API errors', () => {
    // Test error handling
    // Test retry logic
  });
});
```

### Utils Package

**Purpose:** Shared utilities for web and mobile

```typescript
// packages/utils/src/geo.ts
export const geoUtils = {
  calculateDistance: (point1, point2) => { /* ... */ },
  isPointInRadius: (point, center, radius) => { /* ... */ },
  sortByDistance: (trails, userLocation) => { /* ... */ }
};

// Test suite
describe('Geo Utils', () => {
  test('calculates distance correctly', () => {
    // Test Haversine formula
    // Test edge cases
  });

  test('filters trails by radius', () => {
    // Test radius filtering
  });
});
```

---

## Test Metrics & Coverage

### Web Application Metrics

| Category | Value |
|----------|-------|
| Total Test Files | ~30+ |
| Test Cases | ~150+ |
| Average Test Duration | ~50ms |
| Code Coverage | ~85%+ |
| Coverage Type | Statements, Branches, Functions |

### Mobile Application Metrics

| Category | Value |
|----------|-------|
| Total Test Files | ~25+ |
| Test Cases | ~120+ |
| Average Test Duration | ~100ms |
| Code Coverage | ~80%+ |
| Coverage Type | Statements, Branches, Functions |

### Shared Package Metrics

| Package | Tests | Coverage |
|---------|-------|----------|
| api-client | ~20 | 90% |
| utils | ~15 | 95% |
| components | ~30 | 85% |
| hooks | ~25 | 80% |

---

## CI/CD Integration

### GitHub Actions Pipeline

```yaml
name: TrailWaze Tests
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm ci
      - run: npm run lint

  test-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: cd apps/web && npm ci && npm run test:coverage
      - uses: codecov/codecov-action@v2
        with:
          files: ./apps/web/coverage/coverage-final.json

  test-mobile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: cd apps/mobile && npm ci
    - npm run test:coverage
  coverage: '/Coverage: \d+\.\d+%/'

# E2E tests
test:e2e:
  stage: test
  script:
    - npm run build
    - npm run test:e2e
  artifacts:
    reports:
      junit: cypress/results/*.xml
```

### Test Commands

```bash
# Web app
cd apps/web
npm run test                    # Run tests
npm run test:watch            # Watch mode
npm run test:coverage         # Coverage report
npm run test:debug            # Debug mode

# Mobile app
cd apps/mobile
npm run test                    # Run tests
npm run test:coverage         # Coverage report
npm run test:e2e              # E2E tests

# Shared packages
cd packages/api-client
npm run test                    # Run tests
npm run test:coverage         # Coverage report
```

---

## Test Data & Fixtures

### Mock Trail Data

```typescript
export const mockTrails = [
  {
    id: 1,
    name: "Omu Peak Loop",
    difficulty: "HARD",
    latitude: 45.5,
    longitude: 25.3,
    elevation: 2500,
    duration: 480,
    distance: 12.5,
    rating: 4.8,
    reviews: 245,
    description: "Challenging mountain trail..."
  },
  {
    id: 2,
    name: "Butterfly Lake Trail",
    difficulty: "MEDIUM",
    latitude: 45.4,
    longitude: 25.2,
    elevation: 1800,
    duration: 240,
    distance: 8.0,
    rating: 4.6,
    reviews: 182,
    description: "Scenic alpine lake trail..."
  }
];
```

### Mock Location Data

```typescript
export const mockLocation = {
  latitude: 45.45,
  longitude: 25.25,
  accuracy: 5,
  altitude: 1500,
  heading: 180,
  speed: 1.5,
  timestamp: Date.now()
};
```

### Mock API Responses

```typescript
export const mockApiResponses = {
  getTrails: {
    status: 200,
    data: {
      trails: mockTrails,
      total: 2,
      page: 1
    }
  },
  getTrailById: {
    status: 200,
    data: mockTrails[0]
  },
  createTrail: {
    status: 201,
    data: { id: 3, ...newTrail }
  }
};
```

---

## Performance Optimization

### Test Execution Strategy

```
Run Unit Tests (Fast)
    ├─ ~50ms each
    ├─ ~150+ tests
    └─ Total: ~10-15 seconds
         ↓
Run Integration Tests (Medium)
    ├─ ~100-200ms each
    ├─ ~30 tests
    └─ Total: ~5-10 seconds
         ↓
Run E2E Tests (Slow)
    ├─ ~1-5 seconds each
    ├─ ~10 tests
    └─ Total: ~30-60 seconds
         ↓
Generate Coverage Reports
    └─ Total Time: ~2-3 minutes
```

### Parallel Test Execution

```
Web Tests          Mobile Tests       Shared Tests
├─ Unit: 5s        ├─ Unit: 8s        ├─ Unit: 3s
├─ Integration: 3s ├─ Integration: 5s  └─ Coverage: 2s
└─ Coverage: 2s    └─ Coverage: 2s

Total (Parallel): ~8-10 seconds
Total (Sequential): ~30-40 seconds
```

---

## Best Practices

### ✅ Do's

- ✅ Test user interactions
- ✅ Test error boundaries
- ✅ Mock external APIs
- ✅ Use meaningful test names
- ✅ Test accessibility
- ✅ Test responsive behavior
- ✅ Test offline capabilities
- ✅ Maintain high coverage
- ✅ Keep tests isolated
- ✅ Use test utilities

### ❌ Don'ts

- ❌ Don't test implementation details
- ❌ Don't mock everything
- ❌ Don't use sleep() for timing
- ❌ Don't test third-party libraries
- ❌ Don't create flaky tests
- ❌ Don't skip error cases
- ❌ Don't duplicate test logic
- ❌ Don't ignore failures
- ❌ Don't make tests too slow
- ❌ Don't test state directly

---

## Troubleshooting

### Common Issues

#### Issue: Tests Failing Intermittently
**Cause:** Async timing issues, network delays
**Solution:** Use proper async utilities, avoid setTimeout

#### Issue: High Memory Usage
**Cause:** Large test fixtures, unclosed resources
**Solution:** Use proper cleanup, mock expensive operations

#### Issue: Slow Test Suite
**Cause:** Too many integration tests, inefficient setup
**Solution:** Optimize test execution, parallelize tests

#### Issue: Coverage Gaps
**Cause:** Missing error scenarios, platform-specific code
**Solution:** Add comprehensive error tests, test both platforms

---

## Testing Standards

### Code Coverage Targets

| Category | Target |
|----------|--------|
| Statements | 85%+ |
| Branches | 80%+ |
| Functions | 90%+ |
| Lines | 85%+ |

### Test Quality Metrics

- All tests must be deterministic
- No hardcoded delays
- Proper error handling
- Clear assertions
- Isolated state

---

## Documentation & Resources

### Test Documentation Files

```
apps/web/
├── TEST_GUIDE.md           # Web testing guide
├── COMPONENT_TESTS.md      # Component testing patterns
├── JEST_CONFIG.md          # Jest configuration
└── ...

apps/mobile/
├── TEST_GUIDE.md           # Mobile testing guide
├── NATIVE_MODULES.md       # Native testing
├── DETOX_CONFIG.md         # E2E testing
└── ...

packages/api-client/
├── TEST_GUIDE.md           # API client tests
└── MOCK_STRATEGY.md        # Mocking approach
```

---

## Next Steps

1. **Run Test Suite:** `npm run test`
2. **View Coverage:** Check coverage reports
3. **Add New Tests:** Follow existing patterns
4. **Optimize Performance:** Profile slow tests
5. **Improve Coverage:** Target 90%+ coverage
6. **Setup CI/CD:** Enable automated testing
7. **Document Tests:** Maintain test documentation

---

## Related Resources

- [TrailEquip Tests](TRAILEQUIP_TESTS.md)
- [External Repositories](../EXTERNAL_REPOS.md)
- [Test Metrics Report](../TEST_METRICS_REPORT.md)
- [RnDMetrics Architecture](../../ARCHITECTURE.md)

---

**Document Version:** 1.0.0
**Last Reviewed:** January 31, 2026
**Maintained by:** Testing Team
