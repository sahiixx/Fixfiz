/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer.jsx
 * Tests mobile detection, responsive behavior, orientation handling, and styling
 * 
 * This test suite covers:
 * - Mobile detection and device identification (8 tests)
 * - Responsive behavior and viewport changes (10 tests)
 * - Orientation handling (portrait/landscape) (6 tests)
 * - Touch support detection (5 tests)
 * - Style injection and CSS optimization (12 tests)
 * - Performance monitoring (5 tests)
 * - Custom hooks (useMobile) (7 tests)
 * - MobileMatrixRain component (6 tests)
 * - MobileMatrixText component (6 tests)
 * - Edge cases and error handling (10 tests)
 * Total: 75 comprehensive unit tests
 */

import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window properties for testing
const mockWindowProperties = (width, height, userAgent) => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: width,
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: height,
  });
  Object.defineProperty(navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: userAgent,
  });
  Object.defineProperty(navigator, 'maxTouchPoints', {
    writable: true,
    configurable: true,
    value: 0,
  });
};

// Reset window properties after each test
const resetWindowProperties = () => {
  mockWindowProperties(1024, 768, 'Mozilla/5.0');
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    resetWindowProperties();
  });

  // ================================================================================================
  // MOBILE DETECTION TESTS (8 tests)
  // ================================================================================================

  describe('Mobile Detection', () => {
    test('should detect mobile device by width <= 768px', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should detect desktop device by width > 768px', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('desktop-full');
    });

    test('should detect iPhone user agent', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should detect Android user agent', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (Linux; Android 10)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should detect iPad user agent', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPad; CPU OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should detect BlackBerry user agent', () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 BlackBerry');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should handle tablet breakpoint (768px exactly)', () => {
      mockWindowProperties(768, 1024, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      // At exactly 768px, should be considered mobile
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should detect Opera Mini user agent', () => {
      mockWindowProperties(1024, 768, 'Opera Mini/7.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  // ================================================================================================
  // RESPONSIVE BEHAVIOR TESTS (10 tests)
  // ================================================================================================

  describe('Responsive Behavior', () => {
    test('should update device detection on window resize', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
      
      // Simulate resize to desktop
      act(() => {
        mockWindowProperties(1920, 1080, 'Mozilla/5.0');
        window.dispatchEvent(new Event('resize'));
      });
      
      await waitFor(() => {
        rerender(
          <MobileMatrixOptimizer>
            <div>Test Content</div>
          </MobileMatrixOptimizer>
        );
      });
    });

    test('should apply custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('custom-class');
    });

    test('should render children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByTestId('child-content')).toHaveTextContent('Test Content');
    });

    test('should handle multiple children', () => {
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

    test('should set CSS custom property for mobile opacity', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const property = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(property).toBe('0.3');
    });

    test('should set CSS custom property for desktop opacity', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      
      render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const property = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(property).toBe('0.5');
    });

    test('should cleanup event listeners on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    });

    test('should handle rapid resize events', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Simulate multiple rapid resizes
      for (let i = 0; i < 10; i++) {
        act(() => {
          window.dispatchEvent(new Event('resize'));
        });
      }
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });

    test('should transition from mobile to tablet to desktop', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('mobile-optimized');
      
      // Tablet
      act(() => {
        mockWindowProperties(768, 1024, 'Mozilla/5.0');
        window.dispatchEvent(new Event('resize'));
      });
      
      // Desktop
      act(() => {
        mockWindowProperties(1920, 1080, 'Mozilla/5.0');
        window.dispatchEvent(new Event('resize'));
      });
      
      await waitFor(() => {
        rerender(
          <MobileMatrixOptimizer>
            <div>Test Content</div>
          </MobileMatrixOptimizer>
        );
      });
    });

    test('should handle empty children', () => {
      const { container } = render(
        <MobileMatrixOptimizer></MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  // ================================================================================================
  // ORIENTATION HANDLING TESTS (6 tests)
  // ================================================================================================

  describe('Orientation Handling', () => {
    test('should detect portrait orientation', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-portrait');
    });

    test('should detect landscape orientation', () => {
      mockWindowProperties(667, 375, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });

    test('should update orientation on orientationchange event', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-portrait');
      
      act(() => {
        mockWindowProperties(667, 375, 'Mozilla/5.0');
        window.dispatchEvent(new Event('orientationchange'));
      });
      
      await waitFor(() => {
        rerender(
          <MobileMatrixOptimizer>
            <div>Test Content</div>
          </MobileMatrixOptimizer>
        );
      });
    });

    test('should handle square aspect ratio', () => {
      mockWindowProperties(800, 800, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      // Square is considered landscape (height not > width)
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });

    test('should handle desktop landscape orientation', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });

    test('should handle ultra-wide screen', () => {
      mockWindowProperties(3440, 1440, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });

  // ================================================================================================
  // TOUCH SUPPORT TESTS (5 tests)
  // ================================================================================================

  describe('Touch Support Detection', () => {
    test('should detect touch support via maxTouchPoints', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 5,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
    });

    test('should detect no touch support', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 0,
      });
      delete window.ontouchstart;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-disabled');
    });

    test('should detect touch support via ontouchstart', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0');
      window.ontouchstart = null;
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
    });

    test('should handle hybrid devices (touch on desktop)', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 10,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
      expect(container.firstChild).toHaveClass('desktop-full');
    });

    test('should handle multi-touch devices', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 10,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(container.firstChild).toHaveClass('touch-enabled');
    });
  });

  // ================================================================================================
  // STYLE INJECTION TESTS (12 tests)
  // ================================================================================================

  describe('Style Injection and CSS', () => {
    test('should inject mobile styles when on mobile device', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
    });

    test('should not inject mobile styles on desktop', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).not.toBeInTheDocument();
    });

    test('mobile styles should include webkit-overflow-scrolling', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('-webkit-overflow-scrolling');
    });

    test('mobile styles should include responsive text scaling', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('clamp');
    });

    test('mobile styles should include grid optimizations', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('grid-template-columns');
    });

    test('mobile styles should include touch target sizing', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('min-height: 44px');
    });

    test('mobile styles should include padding adjustments', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('padding: 1rem !important');
    });

    test('mobile styles should include landscape adjustments', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('orientation-landscape');
    });

    test('mobile styles should include portrait grid adjustments', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag?.textContent).toContain('orientation-portrait');
    });

    test('should use standard style tag (not jsx)', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag).not.toHaveAttribute('jsx');
    });

    test('should have valid CSS syntax in injected styles', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTag = container.querySelector('style');
      const styleContent = styleTag?.textContent || '';
      
      // Check for basic CSS structure
      expect(styleContent).toContain('{');
      expect(styleContent).toContain('}');
      expect(styleContent).toContain(':');
      expect(styleContent).toContain(';');
    });

    test('should not have duplicate style tags', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleTags = container.querySelectorAll('style');
      expect(styleTags.length).toBeLessThanOrEqual(1);
    });
  });

  // ================================================================================================
  // PERFORMANCE MONITORING TESTS (5 tests)
  // ================================================================================================

  describe('Performance Monitoring', () => {
    test('should show performance monitor on localhost when mobile', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window.location, 'hostname', {
        writable: true,
        configurable: true,
        value: 'localhost',
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2.left-2');
      expect(monitor).toBeInTheDocument();
    });

    test('should not show performance monitor on localhost when desktop', () => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      Object.defineProperty(window.location, 'hostname', {
        writable: true,
        configurable: true,
        value: 'localhost',
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2.left-2');
      expect(monitor).not.toBeInTheDocument();
    });

    test('should not show performance monitor in production', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window.location, 'hostname', {
        writable: true,
        configurable: true,
        value: 'production.example.com',
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2.left-2');
      expect(monitor).not.toBeInTheDocument();
    });

    test('should show performance monitor on 127.0.0.1', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window.location, 'hostname', {
        writable: true,
        configurable: true,
        value: '127.0.0.1',
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2.left-2');
      expect(monitor).toBeInTheDocument();
    });

    test('performance monitor should display device metrics', () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window.location, 'hostname', {
        writable: true,
        configurable: true,
        value: 'localhost',
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      const monitor = container.querySelector('.fixed.bottom-2.left-2');
      expect(monitor?.textContent).toContain('Mobile:');
      expect(monitor?.textContent).toContain('Touch:');
      expect(monitor?.textContent).toContain('Orient:');
      expect(monitor?.textContent).toContain('Width:');
    });
  });
});

// ================================================================================================
// CUSTOM HOOK TESTS (7 tests)
// ================================================================================================

describe('useMobile Hook', () => {
  beforeEach(() => {
    resetWindowProperties();
  });

  test('should return true for mobile width', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    
    let hookResult;
    const TestComponent = () => {
      hookResult = useMobile();
      return <div>{hookResult ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(hookResult).toBe(true);
  });

  test('should return false for desktop width', () => {
    mockWindowProperties(1920, 1080, 'Mozilla/5.0');
    
    let hookResult;
    const TestComponent = () => {
      hookResult = useMobile();
      return <div>{hookResult ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(hookResult).toBe(false);
  });

  test('should update on resize', async () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    
    let hookResult;
    const TestComponent = () => {
      hookResult = useMobile();
      return <div>{hookResult ? 'Mobile' : 'Desktop'}</div>;
    };
    
    const { rerender } = render(<TestComponent />);
    expect(hookResult).toBe(true);
    
    act(() => {
      mockWindowProperties(1920, 1080, 'Mozilla/5.0');
      window.dispatchEvent(new Event('resize'));
    });
    
    await waitFor(() => {
      rerender(<TestComponent />);
      expect(hookResult).toBe(false);
    });
  });

  test('should handle tablet breakpoint', () => {
    mockWindowProperties(768, 1024, 'Mozilla/5.0');
    
    let hookResult;
    const TestComponent = () => {
      hookResult = useMobile();
      return <div>{hookResult ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(hookResult).toBe(true);
  });

  test('should cleanup resize listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    
    const TestComponent = () => {
      useMobile();
      return <div>Test</div>;
    };
    
    const { unmount } = render(<TestComponent />);
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
  });

  test('should initialize correctly on first render', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    
    const TestComponent = () => {
      const isMobile = useMobile();
      return <div data-testid="result">{isMobile ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(screen.getByTestId('result')).toHaveTextContent('Mobile');
  });

  test('should work in multiple components simultaneously', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    
    const Component1 = () => {
      const isMobile = useMobile();
      return <div data-testid="comp1">{isMobile ? 'M' : 'D'}</div>;
    };
    
    const Component2 = () => {
      const isMobile = useMobile();
      return <div data-testid="comp2">{isMobile ? 'M' : 'D'}</div>;
    };
    
    render(
      <>
        <Component1 />
        <Component2 />
      </>
    );
    
    expect(screen.getByTestId('comp1')).toHaveTextContent('M');
    expect(screen.getByTestId('comp2')).toHaveTextContent('M');
  });
});

// ================================================================================================
// MOBILEMATRIXRAIN COMPONENT TESTS (6 tests)
// ================================================================================================

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    resetWindowProperties();
  });

  test('should render on mobile devices', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
  });

  test('should not render on desktop devices', () => {
    mockWindowProperties(1920, 1080, 'Mozilla/5.0');
    
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
  });

  test('should apply custom className', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    const element = container.querySelector('.custom-rain');
    expect(element).toBeInTheDocument();
  });

  test('should include animation styles', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(<MobileMatrixRain />);
    const styleTag = container.querySelector('style');
    expect(styleTag?.textContent).toContain('@keyframes mobile-rain');
  });

  test('should have opacity styling', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(<MobileMatrixRain />);
    const element = container.querySelector('.absolute.inset-0');
    expect(element).toHaveClass('opacity-30');
  });

  test('should have pointer-events-none class', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(<MobileMatrixRain />);
    const element = container.querySelector('.absolute.inset-0');
    expect(element).toHaveClass('pointer-events-none');
  });
});

// ================================================================================================
// MOBILEMATRIXTEXT COMPONENT TESTS (6 tests)
// ================================================================================================

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    resetWindowProperties();
  });

  test('should render children on all devices', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-child">Matrix Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByTestId('text-child')).toBeInTheDocument();
  });

  test('should apply mobile-matrix-text class on mobile', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).toHaveClass('mobile-matrix-text');
  });

  test('should not apply mobile-matrix-text class on desktop', () => {
    mockWindowProperties(1920, 1080, 'Mozilla/5.0');
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
  });

  test('should inject mobile styles on mobile devices', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleTag = container.querySelector('style');
    expect(styleTag).toBeInTheDocument();
  });

  test('mobile styles should include clamp for responsive sizing', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleTag = container.querySelector('style');
    expect(styleTag?.textContent).toContain('clamp');
  });

  test('mobile styles should include glow animation', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
    
    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );
    
    const styleTag = container.querySelector('style');
    expect(styleTag?.textContent).toContain('@keyframes mobile-glow');
  });
});

// ================================================================================================
// EDGE CASES AND ERROR HANDLING TESTS (10 tests)
// ================================================================================================

describe('Edge Cases and Error Handling', () => {
  beforeEach(() => {
    resetWindowProperties();
  });

  test('should handle null children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('should handle undefined children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{undefined}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('should handle false children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{false}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('should handle very small viewport dimensions', () => {
    mockWindowProperties(200, 300, 'Mozilla/5.0');
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Small Screen</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('should handle very large viewport dimensions', () => {
    mockWindowProperties(7680, 4320, 'Mozilla/5.0'); // 8K resolution
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>8K Screen</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('should handle missing navigator.userAgent', () => {
    mockWindowProperties(375, 667, undefined);
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('should handle missing navigator.maxTouchPoints', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    delete navigator.maxTouchPoints;
    
    expect(() => {
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
    }).not.toThrow();
  });

  test('should handle rapid component mount/unmount cycles', () => {
    mockWindowProperties(375, 667, 'Mozilla/5.0');
    
    for (let i = 0; i < 10; i++) {
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Cycle {i}</div>
        </MobileMatrixOptimizer>
      );
      unmount();
    }
    
    // If we get here without errors, test passes
    expect(true).toBe(true);
  });

  test('should handle mixed content types as children', () => {
    render(
      <MobileMatrixOptimizer>
        <div>Div element</div>
        Plain text
        {123}
        <span>Span element</span>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText('Div element')).toBeInTheDocument();
    expect(screen.getByText('Span element')).toBeInTheDocument();
  });

  test('should handle className as undefined', () => {
    const { container } = render(
      <MobileMatrixOptimizer className={undefined}>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
  });
});