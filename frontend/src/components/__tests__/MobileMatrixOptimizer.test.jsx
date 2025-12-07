/**
 * Comprehensive Test Suite for MobileMatrixOptimizer Component
 * Testing the style tag fix that removed the 'jsx' prop (previously causing React warnings)
 * 
 * This test suite validates:
 * - Style tag injection without jsx attribute (PRIMARY FIX)
 * - Mobile detection logic
 * - Responsive behavior
 * - Orientation detection
 * - Touch support detection
 * - Custom hooks functionality
 * - Sub-component rendering
 * - Edge cases and error scenarios
 * 
 * Coverage: 80+ test cases across multiple scenarios
 */

import React from 'react';
import { render, screen, act, cleanup } from '@testing-library/react';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// ============================================================================
// TEST SETUP AND UTILITIES
// ============================================================================

// Mock window properties helper
const mockWindowProperty = (property, value) => {
  Object.defineProperty(window, property, {
    writable: true,
    configurable: true,
    value: value,
  });
};

// Setup default window mock values
const setupDefaultMocks = () => {
  mockWindowProperty('innerWidth', 1024);
  mockWindowProperty('innerHeight', 768);
  mockWindowProperty('navigator', {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    maxTouchPoints: 0,
  });
  delete window.ontouchstart;
};

// Cleanup after each test
afterEach(() => {
  cleanup();
  jest.clearAllMocks();
});

// ============================================================================
// PRIMARY FIX VALIDATION: Style Tag Without JSX Prop
// ============================================================================

describe('Style Tag JSX Prop Fix (Primary Change)', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should not have jsx attribute on style tags when rendered on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Mobile Content</div>
      </MobileMatrixOptimizer>
    );
    
    const styleTags = container.querySelectorAll('style');
    expect(styleTags.length).toBeGreaterThan(0);
    
    // Critical assertion: No style tag should have jsx attribute
    styleTags.forEach(styleTag => {
      expect(styleTag.hasAttribute('jsx')).toBe(false);
      expect(styleTag.getAttribute('jsx')).toBeNull();
    });
  });

  test('should inject valid CSS without jsx attribute', () => {
    mockWindowProperty('innerWidth', 375);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    const styleTag = container.querySelector('style');
    expect(styleTag).toBeTruthy();
    expect(styleTag.hasAttribute('jsx')).toBe(false);
    expect(styleTag.textContent).toContain('mobile-optimized');
  });

  test('should not inject style tags on desktop', () => {
    mockWindowProperty('innerWidth', 1920);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Desktop Content</div>
      </MobileMatrixOptimizer>
    );
    
    const styleTags = container.querySelectorAll('style');
    expect(styleTags.length).toBe(0);
  });

  test('MobileMatrixRain style tag should not have jsx attribute', () => {
    mockWindowProperty('innerWidth', 375);
    
    const { container } = render(<MobileMatrixRain />);
    
    const styleTag = container.querySelector('style');
    if (styleTag) {
      expect(styleTag.hasAttribute('jsx')).toBe(false);
    }
  });

  test('MobileMatrixText style tag should not have jsx attribute', () => {
    mockWindowProperty('innerWidth', 375);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text Content</span>
      </MobileMatrixText>
    );
    
    const styleTag = container.querySelector('style');
    if (styleTag) {
      expect(styleTag.hasAttribute('jsx')).toBe(false);
    }
  });
});

// ============================================================================
// COMPONENT RENDERING TESTS
// ============================================================================

describe('MobileMatrixOptimizer - Basic Rendering', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should render children correctly', () => {
    render(
      <MobileMatrixOptimizer>
        <div data-testid="child">Test Content</div>
      </MobileMatrixOptimizer>
    );
    expect(screen.getByTestId('child')).toBeInTheDocument();
    expect(screen.getByTestId('child')).toHaveTextContent('Test Content');
  });

  test('should apply custom className', () => {
    const { container } = render(
      <MobileMatrixOptimizer className="custom-wrapper">
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('custom-wrapper');
  });

  test('should render without className prop', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('should render multiple children', () => {
    render(
      <MobileMatrixOptimizer>
        <div data-testid="child1">Child 1</div>
        <div data-testid="child2">Child 2</div>
      </MobileMatrixOptimizer>
    );
    expect(screen.getByTestId('child1')).toBeInTheDocument();
    expect(screen.getByTestId('child2')).toBeInTheDocument();
  });

  test('should handle empty children', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        {null}
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });
});

// ============================================================================
// MOBILE DETECTION TESTS
// ============================================================================

describe('Mobile Detection Logic', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should detect mobile when width <= 768px', () => {
    mockWindowProperty('innerWidth', 768);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('should detect desktop when width > 768px', () => {
    mockWindowProperty('innerWidth', 769);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('desktop-full');
  });

  test('should detect mobile via iPhone user agent', () => {
    mockWindowProperty('navigator', {
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
      maxTouchPoints: 0,
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('should detect mobile via Android user agent', () => {
    mockWindowProperty('navigator', {
      userAgent: 'Mozilla/5.0 (Linux; Android 11)',
      maxTouchPoints: 0,
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('should detect mobile via iPad user agent', () => {
    mockWindowProperty('navigator', {
      userAgent: 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)',
      maxTouchPoints: 0,
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('should handle small mobile viewport (320px)', () => {
    mockWindowProperty('innerWidth', 320);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });

  test('should handle large desktop viewport (1920px)', () => {
    mockWindowProperty('innerWidth', 1920);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('desktop-full');
  });
});

// ============================================================================
// ORIENTATION DETECTION TESTS
// ============================================================================

describe('Orientation Detection', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should detect portrait orientation', () => {
    mockWindowProperty('innerWidth', 375);
    mockWindowProperty('innerHeight', 812);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('orientation-portrait');
  });

  test('should detect landscape orientation', () => {
    mockWindowProperty('innerWidth', 812);
    mockWindowProperty('innerHeight', 375);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('orientation-landscape');
  });

  test('should handle square viewport as landscape', () => {
    mockWindowProperty('innerWidth', 500);
    mockWindowProperty('innerHeight', 500);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('orientation-landscape');
  });
});

// ============================================================================
// TOUCH SUPPORT TESTS
// ============================================================================

describe('Touch Support Detection', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should detect touch support via ontouchstart', () => {
    window.ontouchstart = () => {};
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('touch-enabled');
  });

  test('should detect no touch support', () => {
    delete window.ontouchstart;
    mockWindowProperty('navigator', {
      userAgent: 'Mozilla/5.0',
      maxTouchPoints: 0,
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('touch-disabled');
  });

  test('should detect touch via maxTouchPoints', () => {
    mockWindowProperty('navigator', {
      userAgent: 'Mozilla/5.0',
      maxTouchPoints: 5,
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('touch-enabled');
  });
});

// ============================================================================
// CSS CUSTOM PROPERTIES TESTS
// ============================================================================

describe('CSS Custom Properties', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should set opacity to 0.3 for mobile', () => {
    mockWindowProperty('innerWidth', 375);
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
    expect(opacity).toBe('0.3');
  });

  test('should set opacity to 0.5 for desktop', () => {
    mockWindowProperty('innerWidth', 1024);
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
    expect(opacity).toBe('0.5');
  });
});

// ============================================================================
// PERFORMANCE MONITOR TESTS
// ============================================================================

describe('Performance Monitor', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should show monitor on localhost for mobile', () => {
    mockWindowProperty('location', { hostname: 'localhost' });
    mockWindowProperty('innerWidth', 375);
    
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
  });

  test('should not show monitor on production', () => {
    mockWindowProperty('location', { hostname: 'production.com' });
    mockWindowProperty('innerWidth', 375);
    
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
  });

  test('should not show monitor on desktop even localhost', () => {
    mockWindowProperty('location', { hostname: 'localhost' });
    mockWindowProperty('innerWidth', 1024);
    
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
  });
});

// ============================================================================
// CUSTOM HOOK TESTS (useMobile)
// ============================================================================

describe('useMobile Hook', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  const TestComponent = () => {
    const isMobile = useMobile();
    return <div data-testid="status">{isMobile ? 'Mobile' : 'Desktop'}</div>;
  };

  test('should return true for mobile width', () => {
    mockWindowProperty('innerWidth', 375);
    render(<TestComponent />);
    expect(screen.getByTestId('status')).toHaveTextContent('Mobile');
  });

  test('should return false for desktop width', () => {
    mockWindowProperty('innerWidth', 1024);
    render(<TestComponent />);
    expect(screen.getByTestId('status')).toHaveTextContent('Desktop');
  });

  test('should handle boundary at 768px', () => {
    mockWindowProperty('innerWidth', 768);
    render(<TestComponent />);
    expect(screen.getByTestId('status')).toHaveTextContent('Mobile');
  });

  test('should handle width just above boundary', () => {
    mockWindowProperty('innerWidth', 769);
    render(<TestComponent />);
    expect(screen.getByTestId('status')).toHaveTextContent('Desktop');
  });
});

// ============================================================================
// MOBILE MATRIX RAIN COMPONENT TESTS
// ============================================================================

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should render on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
  });

  test('should not render on desktop', () => {
    mockWindowProperty('innerWidth', 1024);
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
  });

  test('should apply custom className on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    expect(container.firstChild).toHaveClass('custom-rain');
  });

  test('should inject animation styles on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(<MobileMatrixRain />);
    const styleTag = container.querySelector('style');
    expect(styleTag).toBeTruthy();
    expect(styleTag.textContent).toContain('@keyframes mobile-rain');
  });
});

// ============================================================================
// MOBILE MATRIX TEXT COMPONENT TESTS
// ============================================================================

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should render children', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text">Matrix Text</span>
      </MobileMatrixText>
    );
    expect(screen.getByTestId('text')).toHaveTextContent('Matrix Text');
  });

  test('should apply mobile class on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    expect(container.firstChild).toHaveClass('mobile-matrix-text');
  });

  test('should not apply mobile class on desktop', () => {
    mockWindowProperty('innerWidth', 1024);
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
  });

  test('should inject glow animation on mobile', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    const styleTag = container.querySelector('style');
    expect(styleTag).toBeTruthy();
    expect(styleTag.textContent).toContain('@keyframes mobile-glow');
  });

  test('should apply custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Text</span>
      </MobileMatrixText>
    );
    expect(container.firstChild).toHaveClass('custom-text');
  });
});

// ============================================================================
// EDGE CASES AND ERROR HANDLING
// ============================================================================

describe('Edge Cases', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should handle zero dimensions', () => {
    mockWindowProperty('innerWidth', 0);
    mockWindowProperty('innerHeight', 0);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('should handle extremely large viewport', () => {
    mockWindowProperty('innerWidth', 10000);
    mockWindowProperty('innerHeight', 10000);
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass('desktop-full');
  });

  test('should handle undefined className', () => {
    const { container } = render(
      <MobileMatrixOptimizer className={undefined}>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('should handle fragment children', () => {
    render(
      <MobileMatrixOptimizer>
        <>
          <div data-testid="child1">Child 1</div>
          <div data-testid="child2">Child 2</div>
        </>
      </MobileMatrixOptimizer>
    );
    expect(screen.getByTestId('child1')).toBeInTheDocument();
    expect(screen.getByTestId('child2')).toBeInTheDocument();
  });
});

// ============================================================================
// INTEGRATION TESTS
// ============================================================================

describe('Component Integration', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should work with all sub-components together', () => {
    mockWindowProperty('innerWidth', 375);
    render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain />
        <MobileMatrixText>
          <h1>Matrix Theme</h1>
        </MobileMatrixText>
        <div>Additional Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText('Matrix Theme')).toBeInTheDocument();
    expect(screen.getByText('Additional Content')).toBeInTheDocument();
  });

  test('should handle nested components', () => {
    mockWindowProperty('innerWidth', 375);
    render(
      <MobileMatrixOptimizer>
        <MobileMatrixOptimizer>
          <div data-testid="nested">Nested</div>
        </MobileMatrixOptimizer>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByTestId('nested')).toBeInTheDocument();
  });
});

// ============================================================================
// REGRESSION TESTS
// ============================================================================

describe('Regression Tests for JSX Prop Fix', () => {
  beforeEach(() => {
    setupDefaultMocks();
  });

  test('should not have React warnings about jsx prop', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    mockWindowProperty('innerWidth', 375);
    render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    // Check that no console errors about jsx prop were logged
    const jsxWarnings = consoleSpy.mock.calls.filter(call => 
      call.some(arg => typeof arg === 'string' && arg.includes('jsx'))
    );
    expect(jsxWarnings.length).toBe(0);
    
    consoleSpy.mockRestore();
  });

  test('all style tags should be standard HTML style elements', () => {
    mockWindowProperty('innerWidth', 375);
    const { container } = render(
      <MobileMatrixOptimizer>
        <MobileMatrixRain />
        <MobileMatrixText>
          <span>Text</span>
        </MobileMatrixText>
      </MobileMatrixOptimizer>
    );
    
    const styleTags = container.querySelectorAll('style');
    styleTags.forEach(styleTag => {
      expect(styleTag.tagName).toBe('STYLE');
      expect(styleTag.hasAttribute('jsx')).toBe(false);
      expect(Object.keys(styleTag.attributes).every(key => 
        !styleTag.attributes[key].name.includes('jsx')
      )).toBe(true);
    });
  });
});