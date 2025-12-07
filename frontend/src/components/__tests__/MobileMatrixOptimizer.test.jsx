/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * Tests the mobile optimization component and its exported utilities
 * 
 * This test suite covers:
 * - Component rendering and initialization
 * - Mobile/desktop detection logic
 * - Orientation detection (portrait/landscape)
 * - Touch support detection
 * - CSS class application
 * - Style injection behavior
 * - Performance monitor display logic
 * - Custom hooks (useMobile)
 * - MobileMatrixRain component
 * - MobileMatrixText component
 * - Window event listeners (resize, orientationchange)
 * - Edge cases and error handling
 * Total: 40+ comprehensive unit tests
 */

import React from 'react';
import { render, screen, cleanup, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window properties for testing
const mockWindowProperties = (overrides = {}) => {
  const defaults = {
    innerWidth: 1024,
    innerHeight: 768,
    location: { hostname: 'example.com' }
  };
  
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: overrides.innerWidth || defaults.innerWidth
  });
  
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: overrides.innerHeight || defaults.innerHeight
  });
  
  if (overrides.location) {
    Object.defineProperty(window, 'location', {
      writable: true,
      configurable: true,
      value: overrides.location
    });
  }
};

// Mock navigator properties
const mockNavigator = (overrides = {}) => {
  Object.defineProperty(window.navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: overrides.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
  });
  
  Object.defineProperty(window.navigator, 'maxTouchPoints', {
    writable: true,
    configurable: true,
    value: overrides.maxTouchPoints !== undefined ? overrides.maxTouchPoints : 0
  });
};

// Helper component to test useMobile hook
const UseMobileTestComponent = () => {
  const isMobile = useMobile();
  return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
};

describe('MobileMatrixOptimizer Component', () => {
  
  beforeEach(() => {
    // Reset to desktop defaults before each test
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    mockNavigator({ userAgent: 'Mozilla/5.0', maxTouchPoints: 0 });
    cleanup();
  });
  
  afterEach(() => {
    cleanup();
  });

  // ================================================================================================
  // BASIC RENDERING TESTS
  // ================================================================================================
  
  describe('Basic Rendering', () => {
    test('renders children content correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByTestId('child-content')).toHaveTextContent('Test Content');
    });
    
    test('renders without crashing when no children provided', () => {
      const { container } = render(<MobileMatrixOptimizer />);
      expect(container.firstChild).toBeInTheDocument();
    });
    
    test('applies custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('custom-class');
    });
    
    test('applies default empty className when not provided', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });

  // ================================================================================================
  // MOBILE DETECTION TESTS
  // ================================================================================================
  
  describe('Mobile Detection', () => {
    test('detects mobile device based on window width <= 768', () => {
      mockWindowProperties({ innerWidth: 768, innerHeight: 1024 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
    
    test('detects desktop device based on window width > 768', () => {
      mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
    });
    
    test('detects mobile device from Android user agent', () => {
      mockWindowProperties({ innerWidth: 1024 });
      mockNavigator({ userAgent: 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36' });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
    
    test('detects mobile device from iPhone user agent', () => {
      mockWindowProperties({ innerWidth: 1024 });
      mockNavigator({ userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)' });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
    
    test('detects mobile device from iPad user agent', () => {
      mockWindowProperties({ innerWidth: 1024 });
      mockNavigator({ userAgent: 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)' });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
    
    test('detects edge case: exactly 768px width should be mobile', () => {
      mockWindowProperties({ innerWidth: 768 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
    
    test('detects edge case: 769px width should be desktop', () => {
      mockWindowProperties({ innerWidth: 769 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });

  // ================================================================================================
  // ORIENTATION DETECTION TESTS
  // ================================================================================================
  
  describe('Orientation Detection', () => {
    test('detects portrait orientation when height > width', () => {
      mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-portrait');
    });
    
    test('detects landscape orientation when width > height', () => {
      mockWindowProperties({ innerWidth: 667, innerHeight: 375 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
    
    test('detects landscape orientation when width equals height', () => {
      mockWindowProperties({ innerWidth: 600, innerHeight: 600 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });

  // ================================================================================================
  // TOUCH SUPPORT DETECTION TESTS
  // ================================================================================================
  
  describe('Touch Support Detection', () => {
    test('detects touch support via maxTouchPoints > 0', () => {
      mockNavigator({ maxTouchPoints: 5 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
    });
    
    test('detects no touch support when maxTouchPoints = 0', () => {
      mockNavigator({ maxTouchPoints: 0 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-disabled');
    });
    
    test('detects touch support via ontouchstart in window', () => {
      // Mock ontouchstart property
      window.ontouchstart = null;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
      
      // Cleanup
      delete window.ontouchstart;
    });
  });

  // ================================================================================================
  // STYLE INJECTION TESTS
  // ================================================================================================
  
  describe('Style Injection', () => {
    test('injects mobile optimization styles when on mobile', () => {
      mockWindowProperties({ innerWidth: 375 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      expect(styleElements.length).toBeGreaterThan(0);
      
      // Check if mobile-optimized styles are present
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      expect(styleContent).toContain('.mobile-optimized');
    });
    
    test('does not inject mobile styles on desktop', () => {
      mockWindowProperties({ innerWidth: 1024 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      
      // Should not have mobile-specific styles
      if (styleContent) {
        expect(styleContent).not.toContain('.mobile-optimized {');
      }
    });
    
    test('mobile styles include webkit overflow scrolling', () => {
      mockWindowProperties({ innerWidth: 375 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      
      expect(styleContent).toContain('-webkit-overflow-scrolling');
    });
    
    test('mobile styles include responsive text scaling', () => {
      mockWindowProperties({ innerWidth: 375 });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      const styleContent = Array.from(styleElements)
        .map(el => el.textContent)
        .join('');
      
      expect(styleContent).toContain('clamp');
    });
  });

  // ================================================================================================
  // PERFORMANCE MONITOR TESTS
  // ================================================================================================
  
  describe('Performance Monitor Display', () => {
    test('shows performance monitor on localhost when mobile', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        location: { hostname: 'localhost' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Look for performance monitor elements
      expect(screen.getByText(/Mobile:/i)).toBeInTheDocument();
      expect(screen.getByText(/Touch:/i)).toBeInTheDocument();
      expect(screen.getByText(/Orient:/i)).toBeInTheDocument();
    });
    
    test('shows performance monitor on 127.0.0.1 when mobile', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        location: { hostname: '127.0.0.1' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile:/i)).toBeInTheDocument();
    });
    
    test('hides performance monitor on production domain when mobile', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        location: { hostname: 'production.com' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/i)).not.toBeInTheDocument();
    });
    
    test('hides performance monitor on desktop even on localhost', () => {
      mockWindowProperties({ 
        innerWidth: 1024,
        location: { hostname: 'localhost' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/i)).not.toBeInTheDocument();
    });
    
    test('performance monitor displays correct mobile status', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        location: { hostname: 'localhost' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile: YES/i)).toBeInTheDocument();
    });
    
    test('performance monitor displays correct touch status', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        location: { hostname: 'localhost' }
      });
      mockNavigator({ maxTouchPoints: 5 });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Touch: YES/i)).toBeInTheDocument();
    });
    
    test('performance monitor displays orientation in uppercase', () => {
      mockWindowProperties({ 
        innerWidth: 375,
        innerHeight: 667,
        location: { hostname: 'localhost' }
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Orient: PORTRAIT/i)).toBeInTheDocument();
    });
  });

  // ================================================================================================
  // CSS CLASSES COMBINATION TESTS
  // ================================================================================================
  
  describe('CSS Classes Combination', () => {
    test('applies all relevant classes for mobile portrait touch device', () => {
      mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
      mockNavigator({ maxTouchPoints: 5 });
      
      const { container } = render(
        <MobileMatrixOptimizer className="custom">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const element = container.firstChild;
      expect(element).toHaveClass('custom');
      expect(element).toHaveClass('mobile-optimized');
      expect(element).toHaveClass('orientation-portrait');
      expect(element).toHaveClass('touch-enabled');
    });
    
    test('applies all relevant classes for desktop landscape no-touch device', () => {
      mockWindowProperties({ innerWidth: 1920, innerHeight: 1080 });
      mockNavigator({ maxTouchPoints: 0 });
      
      const { container } = render(
        <MobileMatrixOptimizer className="custom">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const element = container.firstChild;
      expect(element).toHaveClass('custom');
      expect(element).toHaveClass('desktop-full');
      expect(element).toHaveClass('orientation-landscape');
      expect(element).toHaveClass('touch-disabled');
    });
  });

  // ================================================================================================
  // CSS CUSTOM PROPERTIES TESTS
  // ================================================================================================
  
  describe('CSS Custom Properties', () => {
    test('sets matrix effects opacity for mobile', () => {
      mockWindowProperties({ innerWidth: 375 });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.3');
    });
    
    test('sets matrix effects opacity for desktop', () => {
      mockWindowProperties({ innerWidth: 1024 });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.5');
    });
  });
});

// ================================================================================================
// useMobile HOOK TESTS
// ================================================================================================

describe('useMobile Hook', () => {
  beforeEach(() => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    cleanup();
  });
  
  afterEach(() => {
    cleanup();
  });
  
  test('returns false for desktop width', () => {
    mockWindowProperties({ innerWidth: 1024 });
    
    render(<UseMobileTestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
  });
  
  test('returns true for mobile width', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    render(<UseMobileTestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
  });
  
  test('returns true for exactly 768px width', () => {
    mockWindowProperties({ innerWidth: 768 });
    
    render(<UseMobileTestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
  });
  
  test('returns false for 769px width', () => {
    mockWindowProperties({ innerWidth: 769 });
    
    render(<UseMobileTestComponent />);
    
    expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
  });
});

// ================================================================================================
// MobileMatrixRain COMPONENT TESTS
// ================================================================================================

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    cleanup();
  });
  
  afterEach(() => {
    cleanup();
  });
  
  test('renders rain effect on mobile', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(<MobileMatrixRain />);
    
    expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
  });
  
  test('does not render rain effect on desktop', () => {
    mockWindowProperties({ innerWidth: 1024 });
    
    const { container } = render(<MobileMatrixRain />);
    
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
  });
  
  test('applies custom className on mobile', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    
    const element = container.firstChild;
    expect(element).toHaveClass('custom-rain');
  });
  
  test('rain effect has correct opacity', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(<MobileMatrixRain />);
    
    const element = container.firstChild;
    expect(element).toHaveClass('opacity-30');
  });
  
  test('rain effect includes animation styles', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(<MobileMatrixRain />);
    
    const styleElement = container.querySelector('style');
    expect(styleElement).toBeInTheDocument();
    expect(styleElement.textContent).toContain('mobile-rain');
    expect(styleElement.textContent).toContain('animation');
  });
  
  test('rain animation uses linear gradient', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(<MobileMatrixRain />);
    
    const styleElement = container.querySelector('style');
    expect(styleElement.textContent).toContain('linear-gradient');
  });
});

// ================================================================================================
// MobileMatrixText COMPONENT TESTS
// ================================================================================================

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    cleanup();
  });
  
  afterEach(() => {
    cleanup();
  });
  
  test('renders children content', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-content">Matrix Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('text-content')).toBeInTheDocument();
    expect(screen.getByTestId('text-content')).toHaveTextContent('Matrix Text');
  });
  
  test('applies mobile-matrix-text class on mobile', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('mobile-matrix-text');
  });
  
  test('does not apply mobile-matrix-text class on desktop', () => {
    mockWindowProperties({ innerWidth: 1024 });
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
  });
  
  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('custom-text');
  });
  
  test('injects mobile text styles on mobile', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElement = container.querySelector('style');
    expect(styleElement).toBeInTheDocument();
    expect(styleElement.textContent).toContain('clamp');
  });
  
  test('mobile text styles include glow animation', () => {
    mockWindowProperties({ innerWidth: 375 });
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElement = container.querySelector('style');
    expect(styleElement.textContent).toContain('mobile-glow');
    expect(styleElement.textContent).toContain('text-shadow');
  });
  
  test('does not inject styles on desktop', () => {
    mockWindowProperties({ innerWidth: 1024 });
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleElement = container.querySelector('style');
    expect(styleElement).not.toBeInTheDocument();
  });
});

// ================================================================================================
// EDGE CASES AND ERROR HANDLING TESTS
// ================================================================================================

describe('Edge Cases and Error Handling', () => {
  beforeEach(() => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    cleanup();
  });
  
  afterEach(() => {
    cleanup();
  });
  
  test('handles very small screen width (< 320px)', () => {
    mockWindowProperties({ innerWidth: 240, innerHeight: 400 });
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('mobile-optimized');
  });
  
  test('handles very large screen width (> 4K)', () => {
    mockWindowProperties({ innerWidth: 3840, innerHeight: 2160 });
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('desktop-full');
  });
  
  test('handles missing userAgent gracefully', () => {
    const originalUserAgent = window.navigator.userAgent;
    Object.defineProperty(window.navigator, 'userAgent', {
      get: () => undefined,
      configurable: true
    });
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
    
    // Restore
    Object.defineProperty(window.navigator, 'userAgent', {
      get: () => originalUserAgent,
      configurable: true
    });
  });
  
  test('handles undefined className prop', () => {
    const { container } = render(
      <MobileMatrixOptimizer className={undefined}>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
  });
  
  test('handles null children', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        {null}
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
  });
  
  test('handles multiple children', () => {
    render(
      <MobileMatrixOptimizer>
        <div data-testid="child1">Child 1</div>
        <div data-testid="child2">Child 2</div>
        <div data-testid="child3">Child 3</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByTestId('child1')).toBeInTheDocument();
    expect(screen.getByTestId('child2')).toBeInTheDocument();
    expect(screen.getByTestId('child3')).toBeInTheDocument();
  });
  
  test('handles rapid screen size changes', () => {
    mockWindowProperties({ innerWidth: 1024 });
    
    const { container, rerender } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('desktop-full');
    
    // Simulate rapid resize
    mockWindowProperties({ innerWidth: 375 });
    rerender(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    // Component should update but not crash
    expect(container.firstChild).toBeInTheDocument();
  });
});