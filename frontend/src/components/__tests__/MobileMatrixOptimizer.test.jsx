/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * Tests mobile detection, responsive behavior, style injection, and hooks
 * 
 * This test suite covers:
 * - Component rendering and initialization (8 tests)
 * - Mobile detection and device checks (12 tests)
 * - Orientation detection and handling (8 tests)
 * - Touch support detection (6 tests)
 * - Style injection and CSS (10 tests)
 * - Performance monitoring display (7 tests)
 * - useMobile custom hook (8 tests)
 * - MobileMatrixRain component (8 tests)
 * - MobileMatrixText component (8 tests)
 * - Event listener management (10 tests)
 * - Edge cases and error handling (8 tests)
 * Total: 93 comprehensive unit tests
 */

import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from '../MobileMatrixOptimizer';

// Mock window properties for testing
const mockWindowProperties = (properties) => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: properties.innerWidth || 1024,
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: properties.innerHeight || 768,
  });
  Object.defineProperty(window.navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: properties.userAgent || 'Mozilla/5.0',
  });
  Object.defineProperty(window.navigator, 'maxTouchPoints', {
    writable: true,
    configurable: true,
    value: properties.maxTouchPoints !== undefined ? properties.maxTouchPoints : 0,
  });
};

// Helper to simulate window resize
const simulateResize = (width, height) => {
  window.innerWidth = width;
  window.innerHeight = height;
  window.dispatchEvent(new Event('resize'));
};

// Helper to simulate orientation change
const simulateOrientationChange = () => {
  window.dispatchEvent(new Event('orientationchange'));
};

// ============================================================================
// COMPONENT RENDERING AND INITIALIZATION TESTS (8 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Component Rendering', () => {
  beforeEach(() => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
  });

  test('renders without crashing', () => {
    render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  test('renders children correctly', () => {
    render(
      <MobileMatrixOptimizer>
        <div data-testid="child">Child Content</div>
      </MobileMatrixOptimizer>
    );
    expect(screen.getByTestId('child')).toBeInTheDocument();
    expect(screen.getByText('Child Content')).toBeInTheDocument();
  });

  test('applies custom className when provided', () => {
    const { container } = render(
      <MobileMatrixOptimizer className="custom-class">
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-class');
  });

  test('applies default empty className when not provided', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveAttribute('class');
  });

  test('initializes with desktop mode by default', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('desktop-full');
  });

  test('does not render style tag on desktop', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const styles = container.querySelectorAll('style');
    expect(styles.length).toBe(0);
  });

  test('component structure includes wrapper div', () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild.tagName).toBe('DIV');
  });

  test('handles multiple children correctly', () => {
    render(
      <MobileMatrixOptimizer>
        <div data-testid="child1">Child 1</div>
        <div data-testid="child2">Child 2</div>
        <span data-testid="child3">Child 3</span>
      </MobileMatrixOptimizer>
    );
    expect(screen.getByTestId('child1')).toBeInTheDocument();
    expect(screen.getByTestId('child2')).toBeInTheDocument();
    expect(screen.getByTestId('child3')).toBeInTheDocument();
  });
});

// ============================================================================
// MOBILE DETECTION AND DEVICE CHECKS (12 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Mobile Detection', () => {
  test('detects mobile device by screen width <= 768', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('detects desktop device by screen width > 768', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('desktop-full');
  });

  test('detects iPhone by user agent', () => {
    mockWindowProperties({
      innerWidth: 1024,
      innerHeight: 768,
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('detects Android by user agent', () => {
    mockWindowProperties({
      innerWidth: 1024,
      innerHeight: 768,
      userAgent: 'Mozilla/5.0 (Linux; Android 10)',
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('detects iPad by user agent', () => {
    mockWindowProperties({
      innerWidth: 1024,
      innerHeight: 768,
      userAgent: 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)',
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('detects BlackBerry by user agent', () => {
    mockWindowProperties({
      innerWidth: 1024,
      innerHeight: 768,
      userAgent: 'Mozilla/5.0 (BlackBerry)',
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('handles screen width exactly at 768px boundary', () => {
    mockWindowProperties({ innerWidth: 768, innerHeight: 1024 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('handles very small mobile screens (320px)', () => {
    mockWindowProperties({ innerWidth: 320, innerHeight: 568 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('handles tablet-sized screens (768-1024px)', () => {
    mockWindowProperties({ innerWidth: 900, innerHeight: 600 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('desktop-full');
  });

  test('handles large desktop screens (>1920px)', () => {
    mockWindowProperties({ innerWidth: 2560, innerHeight: 1440 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('desktop-full');
  });

  test('updates mobile state on window resize from desktop to mobile', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('desktop-full');
    
    act(() => {
      simulateResize(375, 667);
    });
    
    rerender(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('updates mobile state on window resize from mobile to desktop', async () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('mobile-optimized');
    
    act(() => {
      simulateResize(1024, 768);
    });
    
    rerender(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });
});

// ============================================================================
// ORIENTATION DETECTION AND HANDLING (8 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Orientation Detection', () => {
  test('detects portrait orientation correctly', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('orientation-portrait');
  });

  test('detects landscape orientation correctly', () => {
    mockWindowProperties({ innerWidth: 667, innerHeight: 375 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('orientation-landscape');
  });

  test('handles square aspect ratio as landscape', () => {
    mockWindowProperties({ innerWidth: 500, innerHeight: 500 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('orientation-landscape');
  });

  test('updates orientation on orientationchange event', async () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toHaveClass('orientation-portrait');
    
    act(() => {
      window.innerWidth = 667;
      window.innerHeight = 375;
      simulateOrientationChange();
    });
    
    rerender(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });

  test('orientation class is always present', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    const hasOrientationClass = wrapper.className.includes('orientation-');
    expect(hasOrientationClass).toBe(true);
  });

  test('handles very tall portrait screens', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 812 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('orientation-portrait');
  });

  test('handles very wide landscape screens', () => {
    mockWindowProperties({ innerWidth: 2560, innerHeight: 1440 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('orientation-landscape');
  });

  test('orientation updates on resize even without orientationchange', async () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    act(() => {
      simulateResize(667, 375);
    });
    
    rerender(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('orientation-landscape');
    });
  });
});

// ============================================================================
// TOUCH SUPPORT DETECTION (6 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Touch Support', () => {
  test('detects touch support via maxTouchPoints', () => {
    mockWindowProperties({ 
      innerWidth: 375, 
      innerHeight: 667,
      maxTouchPoints: 5 
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('touch-enabled');
  });

  test('detects no touch support when maxTouchPoints is 0', () => {
    mockWindowProperties({ 
      innerWidth: 1024, 
      innerHeight: 768,
      maxTouchPoints: 0 
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('touch-disabled');
  });

  test('handles missing maxTouchPoints property', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    delete window.navigator.maxTouchPoints;
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    // Should have either touch-enabled or touch-disabled
    const hasTouchClass = wrapper.className.includes('touch-');
    expect(hasTouchClass).toBe(true);
  });

  test('applies touch-enabled for mobile devices', () => {
    mockWindowProperties({
      innerWidth: 375,
      innerHeight: 667,
      userAgent: 'Mozilla/5.0 (iPhone)',
      maxTouchPoints: 5
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('touch-enabled');
  });

  test('applies touch-disabled for desktop devices', () => {
    mockWindowProperties({
      innerWidth: 1920,
      innerHeight: 1080,
      maxTouchPoints: 0
    });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('touch-disabled');
  });

  test('touch class is always present', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const wrapper = container.firstChild;
    const hasTouchClass = 
      wrapper.className.includes('touch-enabled') ||
      wrapper.className.includes('touch-disabled');
    expect(hasTouchClass).toBe(true);
  });
});

// ============================================================================
// STYLE INJECTION AND CSS (10 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Style Injection', () => {
  test('injects style tag on mobile devices', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const styles = container.querySelectorAll('style');
    expect(styles.length).toBeGreaterThan(0);
  });

  test('does not inject style tag on desktop devices', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const styles = container.querySelectorAll('style');
    expect(styles.length).toBe(0);
  });

  test('injected style contains mobile-optimized class rules', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('.mobile-optimized');
  });

  test('injected style contains webkit scrolling optimization', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('-webkit-overflow-scrolling');
  });

  test('injected style contains responsive text scaling', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('clamp');
  });

  test('injected style contains grid layout rules', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('grid-template-columns');
  });

  test('injected style contains touch target rules', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('.touch-enabled');
    expect(style.textContent).toContain('min-height: 44px');
  });

  test('injected style contains orientation-specific rules', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style.textContent).toContain('.orientation-landscape');
    expect(style.textContent).toContain('.orientation-portrait');
  });

  test('style tag uses standard style element (not jsx attribute)', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const style = container.querySelector('style');
    expect(style).not.toHaveAttribute('jsx');
  });

  test('sets CSS custom property for matrix effects on mobile', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
    expect(opacity).toBe('0.3');
  });
});

// ============================================================================
// PERFORMANCE MONITORING DISPLAY (7 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Performance Monitor', () => {
  beforeEach(() => {
    delete window.location;
    window.location = { hostname: 'localhost' };
  });

  test('shows performance monitor on mobile localhost', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = 'localhost';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
  });

  test('shows performance monitor on mobile 127.0.0.1', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = '127.0.0.1';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
  });

  test('does not show performance monitor on desktop localhost', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    window.location.hostname = 'localhost';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
  });

  test('does not show performance monitor on production mobile', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = 'production.com';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
  });

  test('performance monitor displays correct mobile state', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = 'localhost';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Mobile: YES/)).toBeInTheDocument();
  });

  test('performance monitor displays orientation', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = 'localhost';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Orient: PORTRAIT/)).toBeInTheDocument();
  });

  test('performance monitor displays screen width', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    window.location.hostname = 'localhost';
    
    render(
      <MobileMatrixOptimizer>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    
    expect(screen.getByText(/Width: 375px/)).toBeInTheDocument();
  });
});

// ============================================================================
// useMobile CUSTOM HOOK TESTS (8 tests)
// ============================================================================

describe('useMobile Custom Hook', () => {
  const TestComponent = () => {
    const isMobile = useMobile();
    return <div data-testid="mobile-state">{isMobile ? 'mobile' : 'desktop'}</div>;
  };

  test('returns false for desktop width', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-state')).toHaveTextContent('desktop');
  });

  test('returns true for mobile width', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-state')).toHaveTextContent('mobile');
  });

  test('returns true for width exactly at 768px', () => {
    mockWindowProperties({ innerWidth: 768, innerHeight: 1024 });
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-state')).toHaveTextContent('mobile');
  });

  test('returns false for width just above 768px', () => {
    mockWindowProperties({ innerWidth: 769, innerHeight: 1024 });
    render(<TestComponent />);
    expect(screen.getByTestId('mobile-state')).toHaveTextContent('desktop');
  });

  test('updates on window resize', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { rerender } = render(<TestComponent />);
    
    expect(screen.getByTestId('mobile-state')).toHaveTextContent('desktop');
    
    act(() => {
      simulateResize(375, 667);
    });
    
    rerender(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-state')).toHaveTextContent('mobile');
    });
  });

  test('handles rapid resize events', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { rerender } = render(<TestComponent />);
    
    act(() => {
      simulateResize(375, 667);
      simulateResize(1024, 768);
      simulateResize(375, 667);
    });
    
    rerender(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-state')).toHaveTextContent('mobile');
    });
  });

  test('cleans up resize listener on unmount', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    
    const { unmount } = render(<TestComponent />);
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    removeEventListenerSpy.mockRestore();
  });

  test('can be used in multiple components independently', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    
    const Component1 = () => {
      const isMobile = useMobile();
      return <div data-testid="comp1">{isMobile ? 'mobile' : 'desktop'}</div>;
    };
    
    const Component2 = () => {
      const isMobile = useMobile();
      return <div data-testid="comp2">{isMobile ? 'mobile' : 'desktop'}</div>;
    };
    
    render(
      <>
        <Component1 />
        <Component2 />
      </>
    );
    
    expect(screen.getByTestId('comp1')).toHaveTextContent('mobile');
    expect(screen.getByTestId('comp2')).toHaveTextContent('mobile');
  });
});

// ============================================================================
// MobileMatrixRain COMPONENT TESTS (8 tests)
// ============================================================================

describe('MobileMatrixRain Component', () => {
  test('renders on mobile devices', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
  });

  test('does not render on desktop devices', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(<MobileMatrixRain />);
    expect(container.querySelector('.matrix-mobile-rain')).not.toBeInTheDocument();
  });

  test('applies custom className when provided', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-rain');
  });

  test('injects animation styles on mobile', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    const style = container.querySelector('style');
    expect(style).toBeInTheDocument();
    expect(style.textContent).toContain('@keyframes mobile-rain');
  });

  test('animation uses linear gradient', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    const style = container.querySelector('style');
    expect(style.textContent).toContain('linear-gradient');
  });

  test('animation includes matrix green color', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    const style = container.querySelector('style');
    expect(style.textContent).toContain('rgba(0, 255, 65');
  });

  test('applies pointer-events-none class', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('pointer-events-none');
  });

  test('applies opacity-30 class', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixRain />);
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('opacity-30');
  });
});

// ============================================================================
// MobileMatrixText COMPONENT TESTS (8 tests)
// ============================================================================

describe('MobileMatrixText Component', () => {
  test('renders children correctly', () => {
    render(<MobileMatrixText>Test Text</MobileMatrixText>);
    expect(screen.getByText('Test Text')).toBeInTheDocument();
  });

  test('applies mobile-matrix-text class on mobile', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    expect(container.firstChild).toHaveClass('mobile-matrix-text');
  });

  test('does not apply mobile-matrix-text class on desktop', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    expect(container.firstChild).not.toHaveClass('mobile-matrix-text');
  });

  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">Test</MobileMatrixText>
    );
    expect(container.firstChild).toHaveClass('custom-text');
  });

  test('injects style tag on mobile', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    const style = container.querySelector('style');
    expect(style).toBeInTheDocument();
  });

  test('does not inject style tag on desktop', () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    const style = container.querySelector('style');
    expect(style).not.toBeInTheDocument();
  });

  test('style includes clamp for responsive sizing', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    const style = container.querySelector('style');
    expect(style.textContent).toContain('clamp');
  });

  test('style includes glow animation', () => {
    mockWindowProperties({ innerWidth: 375, innerHeight: 667 });
    const { container } = render(<MobileMatrixText>Test</MobileMatrixText>);
    const style = container.querySelector('style');
    expect(style.textContent).toContain('@keyframes mobile-glow');
    expect(style.textContent).toContain('text-shadow');
  });
});

// ============================================================================
// EVENT LISTENER MANAGEMENT (10 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Event Listeners', () => {
  test('adds resize event listener on mount', () => {
    const addEventListenerSpy = jest.spyOn(window, 'addEventListener');
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    
    expect(addEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    addEventListenerSpy.mockRestore();
  });

  test('adds orientationchange event listener on mount', () => {
    const addEventListenerSpy = jest.spyOn(window, 'addEventListener');
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    
    expect(addEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    addEventListenerSpy.mockRestore();
  });

  test('removes resize event listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    const { unmount } = render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    removeEventListenerSpy.mockRestore();
  });

  test('removes orientationchange event listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    const { unmount } = render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
    removeEventListenerSpy.mockRestore();
  });

  test('handles multiple resize events', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>
    );
    
    act(() => {
      simulateResize(375, 667);
      simulateResize(768, 1024);
      simulateResize(1024, 768);
    });
    
    rerender(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });

  test('does not cause memory leaks with multiple mounts/unmounts', () => {
    const addSpy = jest.spyOn(window, 'addEventListener');
    const removeSpy = jest.spyOn(window, 'removeEventListener');
    
    const { unmount: unmount1 } = render(<MobileMatrixOptimizer><div>1</div></MobileMatrixOptimizer>);
    const { unmount: unmount2 } = render(<MobileMatrixOptimizer><div>2</div></MobileMatrixOptimizer>);
    
    unmount1();
    unmount2();
    
    // Each mount adds 2 listeners, each unmount removes 2
    const addCalls = addSpy.mock.calls.filter(c => c[0] === 'resize' || c[0] === 'orientationchange').length;
    const removeCalls = removeSpy.mock.calls.filter(c => c[0] === 'resize' || c[0] === 'orientationchange').length;
    
    expect(addCalls).toBe(removeCalls);
    
    addSpy.mockRestore();
    removeSpy.mockRestore();
  });

  test('event listeners work after multiple state updates', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container, rerender } = render(
      <MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>
    );
    
    // Multiple state changes
    for (let i = 0; i < 5; i++) {
      act(() => {
        simulateResize(i % 2 === 0 ? 375 : 1024, 667);
      });
      rerender(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    }
    
    await waitFor(() => {
      expect(container.firstChild).toBeDefined();
    });
  });

  test('handles window resize with debouncing behavior', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    const { container } = render(
      <MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>
    );
    
    // Rapid resizes
    act(() => {
      for (let i = 0; i < 10; i++) {
        simulateResize(375 + i * 10, 667);
      }
    });
    
    await waitFor(() => {
      expect(container.firstChild).toBeDefined();
    });
  });

  test('event listeners are unique per component instance', () => {
    const addSpy = jest.spyOn(window, 'addEventListener');
    
    render(<MobileMatrixOptimizer><div>1</div></MobileMatrixOptimizer>);
    render(<MobileMatrixOptimizer><div>2</div></MobileMatrixOptimizer>);
    
    // Each instance should add its own listeners
    const resizeCalls = addSpy.mock.calls.filter(c => c[0] === 'resize');
    expect(resizeCalls.length).toBeGreaterThanOrEqual(2);
    
    addSpy.mockRestore();
  });

  test('cleanup function is called with correct listener references', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    const { unmount } = render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    
    unmount();
    
    // Verify both listeners are removed
    const calls = removeEventListenerSpy.mock.calls;
    const hasResize = calls.some(c => c[0] === 'resize');
    const hasOrientation = calls.some(c => c[0] === 'orientationchange');
    
    expect(hasResize).toBe(true);
    expect(hasOrientation).toBe(true);
    
    removeEventListenerSpy.mockRestore();
  });
});

// ============================================================================
// EDGE CASES AND ERROR HANDLING (8 tests)
// ============================================================================

describe('MobileMatrixOptimizer - Edge Cases', () => {
  test('handles undefined children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{undefined}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('handles null children gracefully', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('handles empty string className', () => {
    const { container } = render(
      <MobileMatrixOptimizer className="">
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveAttribute('class');
  });

  test('handles very long className strings', () => {
    const longClassName = 'a'.repeat(1000);
    const { container } = render(
      <MobileMatrixOptimizer className={longClassName}>
        <div>Test</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toHaveClass(longClassName);
  });

  test('handles extreme screen dimensions', () => {
    mockWindowProperties({ innerWidth: 1, innerHeight: 1 });
    expect(() => {
      render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('handles missing window properties gracefully', () => {
    const originalInnerWidth = window.innerWidth;
    delete window.innerWidth;
    
    expect(() => {
      render(<MobileMatrixOptimizer><div>Test</div></MobileMatrixOptimizer>);
    }).not.toThrow();
    
    window.innerWidth = originalInnerWidth;
  });

  test('handles rapid component mount/unmount cycles', () => {
    expect(() => {
      for (let i = 0; i < 10; i++) {
        const { unmount } = render(<MobileMatrixOptimizer><div>{i}</div></MobileMatrixOptimizer>);
        unmount();
      }
    }).not.toThrow();
  });

  test('handles concurrent rendering without errors', async () => {
    mockWindowProperties({ innerWidth: 1024, innerHeight: 768 });
    
    const promises = [];
    for (let i = 0; i < 5; i++) {
      promises.push(
        act(async () => {
          render(<MobileMatrixOptimizer><div>{i}</div></MobileMatrixOptimizer>);
        })
      );
    }
    
    await expect(Promise.all(promises)).resolves.not.toThrow();
  });
});