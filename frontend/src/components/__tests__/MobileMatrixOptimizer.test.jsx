/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer.jsx
 * Tests mobile detection, responsive behavior, styling injection, and hooks
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
const mockWindowProperties = (width, height, userAgent = '') => {
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
  Object.defineProperty(window.navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: userAgent,
  });
  Object.defineProperty(window.navigator, 'maxTouchPoints', {
    writable: true,
    configurable: true,
    value: 0,
  });
};

// Helper to trigger resize event
const triggerResize = (width, height) => {
  mockWindowProperties(width, height);
  act(() => {
    window.dispatchEvent(new Event('resize'));
  });
};

// Helper to trigger orientation change
const triggerOrientationChange = () => {
  act(() => {
    window.dispatchEvent(new Event('orientationchange'));
  });
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    // Reset window properties before each test
    mockWindowProperties(1920, 1080, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
    // Reset location
    delete window.location;
    window.location = { hostname: 'example.com', href: 'https://example.com' };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Desktop Rendering', () => {
    test('renders children on desktop', () => {
      render(
        <MobileMatrixOptimizer>
          <div>Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText('Test Content')).toBeInTheDocument();
    });

    test('applies desktop classes on desktop viewport', () => {
      const { container } = render(
        <MobileMatrixOptimizer className="test-class">
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('test-class');
      expect(wrapper).toHaveClass('desktop-full');
    });

    test('does not inject mobile styles on desktop', () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      expect(styleElements.length).toBe(0);
    });

    test('does not show performance monitor on desktop', () => {
      window.location.hostname = 'localhost';
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
    });
  });

  describe('Mobile Detection', () => {
    test('detects mobile by viewport width (<= 768px)', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('detects mobile by user agent', async () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('detects Android devices', async () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (Linux; Android 11)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('detects iPad devices', async () => {
      mockWindowProperties(1024, 768, 'Mozilla/5.0 (iPad; CPU OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });
  });

  describe('Touch Support Detection', () => {
    test('detects touch support via ontouchstart', async () => {
      mockWindowProperties(375, 667);
      window.ontouchstart = () => {};
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-enabled');
      });
      
      delete window.ontouchstart;
    });

    test('detects touch support via maxTouchPoints', async () => {
      mockWindowProperties(375, 667);
      Object.defineProperty(window.navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 5,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-enabled');
      });
    });

    test('applies touch-disabled class when no touch support', async () => {
      mockWindowProperties(1920, 1080);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('touch-disabled');
      });
    });
  });

  describe('Orientation Detection', () => {
    test('detects portrait orientation (height > width)', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('orientation-portrait');
      });
    });

    test('detects landscape orientation (width > height)', async () => {
      mockWindowProperties(667, 375);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const wrapper = container.firstChild;
        expect(wrapper).toHaveClass('orientation-landscape');
      });
    });

    test('responds to orientation change event', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-portrait');
      });
      
      // Change to landscape
      mockWindowProperties(667, 375);
      triggerOrientationChange();
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('orientation-landscape');
      });
    });
  });

  describe('Responsive Behavior', () => {
    test('updates classes on window resize from desktop to mobile', async () => {
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
      });
      
      // Resize to mobile
      triggerResize(375, 667);
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
    });

    test('updates classes on window resize from mobile to desktop', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('mobile-optimized');
      });
      
      // Resize to desktop
      triggerResize(1920, 1080);
      
      await waitFor(() => {
        expect(container.firstChild).toHaveClass('desktop-full');
      });
    });
  });

  describe('Style Injection', () => {
    test('injects style tag on mobile', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const styleElements = container.querySelectorAll('style');
        expect(styleElements.length).toBeGreaterThan(0);
      });
    });

    test('style tag uses standard <style> without jsx attribute', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const styleElements = container.querySelectorAll('style');
        styleElements.forEach(style => {
          // Ensure no 'jsx' attribute is present
          expect(style.hasAttribute('jsx')).toBe(false);
        });
      });
    });

    test('injected styles contain mobile optimization rules', async () => {
      mockWindowProperties(375, 667);
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const styleElement = container.querySelector('style');
        expect(styleElement).toBeInTheDocument();
        const styleContent = styleElement.textContent;
        
        // Check for key mobile optimization CSS
        expect(styleContent).toContain('.mobile-optimized');
        expect(styleContent).toContain('-webkit-overflow-scrolling');
        expect(styleContent).toContain('scroll-behavior');
      });
    });

    test('injected styles contain touch target rules', async () => {
      mockWindowProperties(375, 667);
      window.ontouchstart = () => {};
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const styleElement = container.querySelector('style');
        const styleContent = styleElement.textContent;
        
        expect(styleContent).toContain('.touch-enabled');
        expect(styleContent).toContain('min-height: 44px');
        expect(styleContent).toContain('min-width: 44px');
      });
      
      delete window.ontouchstart;
    });
  });

  describe('CSS Custom Properties', () => {
    test('sets CSS custom property for mobile effects opacity', async () => {
      mockWindowProperties(375, 667);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacity).toBe('0.3');
      });
    });

    test('sets CSS custom property for desktop effects opacity', async () => {
      mockWindowProperties(1920, 1080);
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
        expect(opacity).toBe('0.5');
      });
    });
  });

  describe('Performance Monitor', () => {
    test('shows performance monitor on mobile localhost', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      window.location.hostname = 'localhost';
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
        expect(screen.getByText(/Touch:/)).toBeInTheDocument();
        expect(screen.getByText(/Orient:/)).toBeInTheDocument();
        expect(screen.getByText(/Width:/)).toBeInTheDocument();
      });
    });

    test('shows performance monitor on mobile 127.0.0.1', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      window.location.hostname = '127.0.0.1';
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
      });
    });

    test('does not show performance monitor on production domain', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      window.location.hostname = 'create-25.preview.emergentagent.com';
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
      });
    });

    test('performance monitor displays correct values', async () => {
      mockWindowProperties(375, 667, 'Mozilla/5.0 (iPhone)');
      window.location.hostname = 'localhost';
      window.ontouchstart = () => {};
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      await waitFor(() => {
        expect(screen.getByText('Mobile: YES')).toBeInTheDocument();
        expect(screen.getByText('Touch: YES')).toBeInTheDocument();
        expect(screen.getByText('Orient: PORTRAIT')).toBeInTheDocument();
        expect(screen.getByText('Width: 375px')).toBeInTheDocument();
      });
      
      delete window.ontouchstart;
    });
  });

  describe('Event Listeners Cleanup', () => {
    test('cleans up resize event listener on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
      
      removeEventListenerSpy.mockRestore();
    });

    test('cleans up orientationchange event listener on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
      
      removeEventListenerSpy.mockRestore();
    });
  });
});

describe('useMobile Hook', () => {
  const TestComponent = () => {
    const isMobile = useMobile();
    return <div data-testid="mobile-status">{isMobile ? 'mobile' : 'desktop'}</div>;
  };

  beforeEach(() => {
    mockWindowProperties(1920, 1080);
  });

  test('returns false for desktop viewport', async () => {
    render(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });
  });

  test('returns true for mobile viewport (<=768px)', async () => {
    mockWindowProperties(375, 667);
    
    render(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('updates on window resize', async () => {
    const { rerender } = render(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('desktop');
    });
    
    triggerResize(375, 667);
    rerender(<TestComponent />);
    
    await waitFor(() => {
      expect(screen.getByTestId('mobile-status')).toHaveTextContent('mobile');
    });
  });

  test('cleans up resize listener on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
    
    const { unmount } = render(<TestComponent />);
    unmount();
    
    expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
    
    removeEventListenerSpy.mockRestore();
  });
});

describe('MobileMatrixRain Component', () => {
  beforeEach(() => {
    mockWindowProperties(1920, 1080);
  });

  test('renders null on desktop', () => {
    const { container } = render(<MobileMatrixRain />);
    expect(container.firstChild).toBeNull();
  });

  test('renders rain effect on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      expect(container.querySelector('.matrix-mobile-rain')).toBeInTheDocument();
    });
  });

  test('applies custom className on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    
    await waitFor(() => {
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('custom-rain');
    });
  });

  test('injects animation styles on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      const styleContent = styleElement.textContent;
      
      expect(styleContent).toContain('@keyframes mobile-rain');
      expect(styleContent).toContain('animation: mobile-rain');
    });
  });

  test('style tag does not have jsx attribute', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement.hasAttribute('jsx')).toBe(false);
    });
  });
});

describe('MobileMatrixText Component', () => {
  beforeEach(() => {
    mockWindowProperties(1920, 1080);
  });

  test('renders children on desktop', () => {
    render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByText('Test Text')).toBeInTheDocument();
  });

  test('renders children on mobile', async () => {
    mockWindowProperties(375, 667);
    
    render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Test Text')).toBeInTheDocument();
    });
  });

  test('applies mobile-matrix-text class on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-matrix-text');
    });
  });

  test('applies custom className', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('custom-text');
    });
  });

  test('injects responsive text styles on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      const styleContent = styleElement.textContent;
      
      expect(styleContent).toContain('.mobile-matrix-text');
      expect(styleContent).toContain('font-size: clamp');
    });
  });

  test('injects glow animation styles on mobile', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const styleElement = container.querySelector('style');
      const styleContent = styleElement.textContent;
      
      expect(styleContent).toContain('@keyframes mobile-glow');
      expect(styleContent).toContain('text-shadow');
    });
  });

  test('style tag does not have jsx attribute', async () => {
    mockWindowProperties(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    await waitFor(() => {
      const styleElement = container.querySelector('style');
      expect(styleElement.hasAttribute('jsx')).toBe(false);
    });
  });

  test('does not inject styles on desktop', () => {
    const { container } = render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    const styleElements = container.querySelectorAll('style');
    expect(styleElements.length).toBe(0);
  });
});

describe('Edge Cases and Error Handling', () => {
  beforeEach(() => {
    mockWindowProperties(1920, 1080);
  });

  test('handles missing children gracefully', () => {
    const { container } = render(<MobileMatrixOptimizer />);
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles empty className prop', () => {
    const { container } = render(
      <MobileMatrixOptimizer className="">
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    expect(container.firstChild).toBeInTheDocument();
  });

  test('handles multiple rapid resizes', async () => {
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    // Trigger multiple rapid resizes
    triggerResize(375, 667);
    triggerResize(1920, 1080);
    triggerResize(768, 1024);
    triggerResize(375, 667);
    
    await waitFor(() => {
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('handles boundary viewport width (768px)', async () => {
    mockWindowProperties(768, 1024);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      // 768px should be considered mobile (<=768)
      expect(container.firstChild).toHaveClass('mobile-optimized');
    });
  });

  test('handles boundary viewport width (769px)', async () => {
    mockWindowProperties(769, 1024);
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
        </MobileMatrixOptimizer>
    );
    
    await waitFor(() => {
      // 769px should be considered desktop (>768)
      expect(container.firstChild).toHaveClass('desktop-full');
    });
  });
});