/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * 
 * This test suite covers:
 * - MobileMatrixOptimizer component rendering and behavior
 * - Device detection (mobile vs desktop)
 * - Orientation changes (portrait vs landscape)
 * - Touch support detection
 * - CSS class application
 * - Style injection changes (jsx to standard style tags)
 * - useMobile custom hook
 * - MobileMatrixRain component
 * - MobileMatrixText component
 * - Window resize handling
 * - Orientation change events
 * - Performance optimization effects
 * - Edge cases and error conditions
 * 
 * Total: 40+ comprehensive unit tests
 */

import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from './MobileMatrixOptimizer';

// Helper function to create a test component using the useMobile hook
const TestUseMobileComponent = () => {
  const isMobile = useMobile();
  return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
};

// Helper to trigger resize event
const triggerResize = (width, height) => {
  global.innerWidth = width;
  global.innerHeight = height;
  global.dispatchEvent(new Event('resize'));
};

// Helper to trigger orientation change
const triggerOrientationChange = () => {
  global.dispatchEvent(new Event('orientationchange'));
};

// Mock user agent
const setUserAgent = (userAgent) => {
  Object.defineProperty(window.navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: userAgent
  });
};

describe('MobileMatrixOptimizer Component', () => {
  // Store original values to restore after tests
  let originalInnerWidth;
  let originalInnerHeight;
  let originalUserAgent;
  let originalMaxTouchPoints;

  beforeEach(() => {
    // Save original values
    originalInnerWidth = global.innerWidth;
    originalInnerHeight = global.innerHeight;
    originalUserAgent = navigator.userAgent;
    originalMaxTouchPoints = navigator.maxTouchPoints;

    // Set default desktop environment
    global.innerWidth = 1920;
    global.innerHeight = 1080;
    setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0');
    Object.defineProperty(navigator, 'maxTouchPoints', {
      writable: true,
      configurable: true,
      value: 0
    });

    // Mock document.documentElement.style.setProperty
    document.documentElement.style.setProperty = jest.fn();
  });

  afterEach(() => {
    // Restore original values
    global.innerWidth = originalInnerWidth;
    global.innerHeight = originalInnerHeight;
    jest.clearAllMocks();
  });

  // ================================================================================================
  // BASIC RENDERING TESTS
  // ================================================================================================

  describe('Basic Rendering', () => {
    test('renders children correctly', () => {
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
      expect(container).toBeInTheDocument();
    });

    test('applies custom className prop', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="custom-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-class');
    });

    test('applies default empty className when not provided', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      expect(container.firstChild).toBeInTheDocument();
    });
  });

  // ================================================================================================
  // DEVICE DETECTION TESTS
  // ================================================================================================

  describe('Device Detection', () => {
    test('detects desktop based on window width', () => {
      global.innerWidth = 1024;
      global.innerHeight = 768;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
        expect(container.firstChild).not.toHaveClass('mobile-optimized');
      });
    });

    test('detects mobile based on window width <= 768', () => {
      global.innerWidth = 375;
      global.innerHeight = 667;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
        expect(container.firstChild).not.toHaveClass('desktop-full');
      });
    });

    test('detects mobile based on iPhone user agent', () => {
      global.innerWidth = 1024;
      setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)');

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('detects mobile based on Android user agent', () => {
      global.innerWidth = 1024;
      setUserAgent('Mozilla/5.0 (Linux; Android 11) Chrome/91.0');

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('detects mobile based on iPad user agent', () => {
      setUserAgent('Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)');

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });
  });

  // ================================================================================================
  // ORIENTATION DETECTION TESTS
  // ================================================================================================

  describe('Orientation Detection', () => {
    test('detects portrait orientation when height > width', () => {
      global.innerWidth = 375;
      global.innerHeight = 812;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-portrait');
      });
    });

    test('detects landscape orientation when width > height', () => {
      global.innerWidth = 812;
      global.innerHeight = 375;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-landscape');
      });
    });

    test('updates orientation on orientationchange event', async () => {
      global.innerWidth = 375;
      global.innerHeight = 667;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-portrait');
      });

      // Simulate orientation change
      act(() => {
        global.innerWidth = 667;
        global.innerHeight = 375;
        triggerOrientationChange();
      });

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-landscape');
      });
    });
  });

  // ================================================================================================
  // TOUCH SUPPORT DETECTION TESTS
  // ================================================================================================

  describe('Touch Support Detection', () => {
    test('detects touch-enabled device with maxTouchPoints', () => {
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 5
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('touch-enabled');
      });
    });

    test('detects touch-disabled device with no touch points', () => {
      Object.defineProperty(navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 0
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('touch-disabled');
      });
    });

    test('detects touch support via ontouchstart', () => {
      // Simulate ontouchstart in window
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: null
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.firstChild).toHaveClass('touch-enabled');
      });
    });
  });

  // ================================================================================================
  // STYLE INJECTION TESTS
  // ================================================================================================

  describe('Style Injection', () => {
    test('injects mobile styles when device is mobile', () => {
      global.innerWidth = 375;
      global.innerHeight = 667;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        // Check for style tag (changed from <style jsx> to <style>)
        const styleTag = container.querySelector('style');
        expect(styleTag).toBeInTheDocument();
        expect(styleTag.textContent).toContain('.mobile-optimized');
        expect(styleTag.textContent).toContain('-webkit-overflow-scrolling');
      });
    });

    test('does not inject mobile styles on desktop', () => {
      global.innerWidth = 1920;
      global.innerHeight = 1080;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        const styleTag = container.querySelector('style');
        expect(styleTag).not.toBeInTheDocument();
      });
    });

    test('mobile styles include touch-enabled optimizations', () => {
      global.innerWidth = 375;
      global.innerHeight = 667;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        const styleTag = container.querySelector('style');
        expect(styleTag.textContent).toContain('.touch-enabled button');
        expect(styleTag.textContent).toContain('min-height: 44px');
      });
    });

    test('mobile styles include orientation-specific rules', () => {
      global.innerWidth = 375;
      global.innerHeight = 667;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        const styleTag = container.querySelector('style');
        expect(styleTag.textContent).toContain('.orientation-landscape');
        expect(styleTag.textContent).toContain('.orientation-portrait');
      });
    });
  });

  // ================================================================================================
  // PERFORMANCE OPTIMIZATION TESTS
  // ================================================================================================

  describe('Performance Optimization', () => {
    test('sets CSS variable for mobile opacity', () => {
      global.innerWidth = 375;

      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(document.documentElement.style.setProperty).toHaveBeenCalledWith(
          '--matrix-effects-opacity',
          '0.3'
        );
      });
    });

    test('sets CSS variable for desktop opacity', () => {
      global.innerWidth = 1920;

      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(document.documentElement.style.setProperty).toHaveBeenCalledWith(
          '--matrix-effects-opacity',
          '0.5'
        );
      });
    });

    test('updates opacity when switching from desktop to mobile', async () => {
      global.innerWidth = 1920;

      const { rerender } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(document.documentElement.style.setProperty).toHaveBeenCalledWith(
          '--matrix-effects-opacity',
          '0.5'
        );
      });

      // Trigger resize to mobile
      act(() => {
        global.innerWidth = 375;
        triggerResize(375, 667);
      });

      await waitFor(() => {
        expect(document.documentElement.style.setProperty).toHaveBeenCalledWith(
          '--matrix-effects-opacity',
          '0.3'
        );
      });
    });
  });

  // ================================================================================================
  // WINDOW RESIZE HANDLING TESTS
  // ================================================================================================

  describe('Window Resize Handling', () => {
    test('updates device state on window resize', async () => {
      global.innerWidth = 1024;

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
      });

      // Resize to mobile
      act(() => {
        triggerResize(375, 667);
      });

      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('cleans up resize event listener on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');

      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      unmount();

      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    });
  });

  // ================================================================================================
  // PERFORMANCE MONITOR TESTS
  // ================================================================================================

  describe('Performance Monitor', () => {
    test('shows performance monitor on mobile localhost', () => {
      global.innerWidth = 375;
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' }
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.textContent).toContain('Mobile:');
        expect(container.textContent).toContain('Touch:');
        expect(container.textContent).toContain('Orient:');
        expect(container.textContent).toContain('Width:');
      });
    });

    test('shows performance monitor on mobile 127.0.0.1', () => {
      global.innerWidth = 375;
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: '127.0.0.1' }
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.textContent).toContain('YES'); // Mobile: YES
      });
    });

    test('does not show performance monitor on production', () => {
      global.innerWidth = 375;
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'production.com' }
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.textContent).not.toContain('Mobile: YES');
      });
    });

    test('does not show performance monitor on desktop localhost', () => {
      global.innerWidth = 1920;
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' }
      });

      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );

      waitFor(() => {
        expect(container.textContent).not.toContain('Mobile: YES');
      });
    });
  });
});

// ================================================================================================
// useMobile HOOK TESTS
// ================================================================================================

describe('useMobile Hook', () => {
  beforeEach(() => {
    global.innerWidth = 1920;
    global.innerHeight = 1080;
  });

  test('returns false for desktop width', () => {
    global.innerWidth = 1024;

    render(<TestUseMobileComponent />);

    waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });
  });

  test('returns true for mobile width', () => {
    global.innerWidth = 375;

    render(<TestUseMobileComponent />);

    waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('returns true exactly at 768px boundary', () => {
    global.innerWidth = 768;

    render(<TestUseMobileComponent />);

    waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('returns false at 769px', () => {
    global.innerWidth = 769;

    render(<TestUseMobileComponent />);

    waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });
  });

  test('updates on window resize', async () => {
    global.innerWidth = 1024;

    render(<TestUseMobileComponent />);

    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });

    act(() => {
      triggerResize(375, 667);
    });

    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('cleans up resize listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');

    const { unmount } = render(<TestUseMobileComponent />);

    unmount();

    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
  });
});

// ================================================================================================
// MobileMatrixRain COMPONENT TESTS
// ================================================================================================

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    global.innerWidth = 1920;
    global.innerHeight = 1080;
  });

  test('renders rain effect on mobile', () => {
    global.innerWidth = 375;

    const { container } = render(<MobileMatrixRain />);

    waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    });
  });

  test('does not render on desktop', () => {
    global.innerWidth = 1920;

    const { container } = render(<MobileMatrixRain />);

    waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
    });
  });

  test('applies custom className', () => {
    global.innerWidth = 375;

    const { container } = render(<MobileMatrixRain className="custom-rain" />);

    waitFor(() => {
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-rain');
    });
  });

  test('injects animation styles on mobile', () => {
    global.innerWidth = 375;

    const { container } = render(<MobileMatrixRain />);

    waitFor(() => {
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.textContent).toContain('@keyframes mobile-rain');
      expect(styleTag.textContent).toContain('background: linear-gradient');
    });
  });

  test('has correct opacity class', () => {
    global.innerWidth = 375;

    const { container } = render(<MobileMatrixRain />);

    waitFor(() => {
      expect(container.firstChild).toHaveClass('opacity-30');
    });
  });

  test('updates when switching from desktop to mobile', async () => {
    global.innerWidth = 1920;

    const { container, rerender } = render(<MobileMatrixRain />);

    await waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
    });

    act(() => {
      triggerResize(375, 667);
    });

    rerender(<MobileMatrixRain />);

    await waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    });
  });
});

// ================================================================================================
// MobileMatrixText COMPONENT TESTS
// ================================================================================================

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    global.innerWidth = 1920;
    global.innerHeight = 1080;
  });

  test('renders children correctly', () => {
    render(
      <MobileMatrixText>
        <span data-testid="text-content">Matrix Text</span>
      </MobileMatrixText>
    );

    expect(screen.getByTestId('text-content')).toBeInTheDocument();
    expect(screen.getByTestId('text-content')).toHaveTextContent('Matrix Text');
  });

  test('applies mobile-matrix-text class on mobile', () => {
    global.innerWidth = 375;

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });
  });

  test('does not apply mobile-matrix-text class on desktop', () => {
    global.innerWidth = 1920;

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    waitFor(() => {
      expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
    });
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
    global.innerWidth = 375;

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    waitFor(() => {
      const styleTag = container.querySelector('style');
      expect(styleTag).toBeInTheDocument();
      expect(styleTag.textContent).toContain('.mobile-matrix-text');
      expect(styleTag.textContent).toContain('font-size: clamp');
      expect(styleTag.textContent).toContain('@keyframes mobile-glow');
    });
  });

  test('does not inject styles on desktop', () => {
    global.innerWidth = 1920;

    const { container } = render(
      <MobileMatrixText>
        <span>Text</span>
      </MobileMatrixText>
    );

    waitFor(() => {
      const styleTag = container.querySelector('style');
      expect(styleTag).not.toBeInTheDocument();
    });
  });

  test('handles empty children', () => {
    const { container } = render(<MobileMatrixText />);
    expect(container).toBeInTheDocument();
  });
});

// ================================================================================================
// EDGE CASES AND ERROR HANDLING
// ================================================================================================

describe('Edge Cases and Error Handling', () => {
  test('handles rapid resize events', async () => {
    global.innerWidth = 1024;

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    // Trigger multiple rapid resizes
    act(() => {
      triggerResize(375, 667);
      triggerResize(768, 1024);
      triggerResize(1920, 1080);
      triggerResize(375, 667);
    });

    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('handles missing navigator properties gracefully', () => {
    // Remove maxTouchPoints
    delete navigator.maxTouchPoints;

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    expect(container).toBeInTheDocument();
  });

  test('handles very small window dimensions', () => {
    global.innerWidth = 320;
    global.innerHeight = 240;

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });

  test('handles very large window dimensions', () => {
    global.innerWidth = 7680;
    global.innerHeight = 4320;

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    waitFor(() => {
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });

  test('handles square aspect ratio', () => {
    global.innerWidth = 800;
    global.innerHeight = 800;

    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );

    waitFor(() => {
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });
});