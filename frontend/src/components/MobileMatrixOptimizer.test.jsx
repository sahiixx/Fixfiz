/**
 * Comprehensive Unit Tests for MobileMatrixOptimizer Component
 * 
 * NOTE: This test file requires React Testing Library to be installed.
 * Install with: npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
 * 
 * These tests cover:
 * - Mobile device detection
 * - Touch support detection
 * - Orientation detection
 * - CSS injection
 * - Performance monitoring display
 * - Custom hooks
 * - Responsive behavior
 * - Edge cases
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MobileMatrixOptimizer, { 
  useMobile, 
  MobileMatrixRain, 
  MobileMatrixText 
} from './MobileMatrixOptimizer';

// Mock window properties
const mockWindow = (width, height, userAgent = 'desktop') => {
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
};

describe('MobileMatrixOptimizer Component', () => {
  beforeEach(() => {
    // Reset window dimensions before each test
    mockWindow(1920, 1080, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
  });

  describe('Initial Rendering', () => {
    test('renders children correctly', () => {
      render(
        <MobileMatrixOptimizer>
          <div data-testid="child-content">Test Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByTestId('child-content')).toBeInTheDocument();
      expect(screen.getByText('Test Content')).toBeInTheDocument();
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

    test('renders without crashing with no props', () => {
      expect(() => {
        render(
          <MobileMatrixOptimizer>
            <div>Content</div>
          </MobileMatrixOptimizer>
        );
      }).not.toThrow();
    });
  });

  describe('Desktop Detection', () => {
    test('detects desktop device correctly', () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('desktop-full');
      expect(wrapper).not.toHaveClass('mobile-optimized');
    });

    test('applies landscape orientation class on desktop', () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('orientation-landscape');
    });

    test('does not inject mobile styles on desktop', () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElements = container.querySelectorAll('style');
      expect(styleElements.length).toBe(0);
    });
  });

  describe('Mobile Detection', () => {
    test('detects mobile device by width', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('mobile-optimized');
      expect(wrapper).not.toHaveClass('desktop-full');
    });

    test('detects iPhone user agent', () => {
      mockWindow(1024, 768, 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('mobile-optimized');
    });

    test('detects Android user agent', () => {
      mockWindow(1024, 768, 'Mozilla/5.0 (Linux; Android 10)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('mobile-optimized');
    });

    test('detects iPad user agent', () => {
      mockWindow(1024, 1366, 'Mozilla/5.0 (iPad; CPU OS 14_0)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('mobile-optimized');
    });

    test('injects mobile styles on mobile device', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const styleElement = container.querySelector('style');
      expect(styleElement).toBeInTheDocument();
      expect(styleElement.textContent).toContain('.mobile-optimized');
    });
  });

  describe('Orientation Detection', () => {
    test('detects portrait orientation', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)'); // height > width
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('orientation-portrait');
    });

    test('detects landscape orientation', () => {
      mockWindow(667, 375, 'Mozilla/5.0 (iPhone)'); // width > height
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('orientation-landscape');
    });
  });

  describe('Touch Support Detection', () => {
    test('detects touch support', () => {
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: null,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('touch-enabled');
    });

    test('detects no touch support', () => {
      Object.defineProperty(window, 'ontouchstart', {
        writable: true,
        configurable: true,
        value: undefined,
      });
      Object.defineProperty(window.navigator, 'maxTouchPoints', {
        writable: true,
        configurable: true,
        value: 0,
      });
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('touch-disabled');
    });
  });

  describe('Responsive Behavior', () => {
    test('updates on window resize', async () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows)');
      
      const { container, rerender } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      let wrapper = container.firstChild;
      expect(wrapper).toHaveClass('desktop-full');
      
      // Simulate resize to mobile
      mockWindow(375, 667, 'Mozilla/5.0 (Windows)');
      fireEvent(window, new Event('resize'));
      
      await waitFor(() => {
        wrapper = container.firstChild;
        expect(wrapper).toHaveClass('mobile-optimized');
      });
    });

    test('updates on orientation change', async () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)');
      
      const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      let wrapper = container.firstChild;
      expect(wrapper).toHaveClass('orientation-portrait');
      
      // Simulate orientation change
      mockWindow(667, 375, 'Mozilla/5.0 (iPhone)');
      fireEvent(window, new Event('orientationchange'));
      
      await waitFor(() => {
        wrapper = container.firstChild;
        expect(wrapper).toHaveClass('orientation-landscape');
      });
    });
  });

  describe('CSS Custom Properties', () => {
    test('sets matrix effects opacity for mobile', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)');
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.3');
    });

    test('sets matrix effects opacity for desktop', () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows)');
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const opacity = document.documentElement.style.getPropertyValue('--matrix-effects-opacity');
      expect(opacity).toBe('0.5');
    });
  });

  describe('Performance Monitor', () => {
    test('shows performance monitor on localhost mobile', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.getByText(/Mobile:/)).toBeInTheDocument();
      expect(screen.getByText(/Touch:/)).toBeInTheDocument();
      expect(screen.getByText(/Orient:/)).toBeInTheDocument();
    });

    test('hides performance monitor on production mobile', () => {
      mockWindow(375, 667, 'Mozilla/5.0 (iPhone)');
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'example.com' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
    });

    test('hides performance monitor on desktop localhost', () => {
      mockWindow(1920, 1080, 'Mozilla/5.0 (Windows)');
      Object.defineProperty(window, 'location', {
        writable: true,
        value: { hostname: 'localhost' },
      });
      
      render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      expect(screen.queryByText(/Mobile:/)).not.toBeInTheDocument();
    });
  });

  describe('Event Cleanup', () => {
    test('removes event listeners on unmount', () => {
      const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');
      
      const { unmount } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      unmount();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith('resize', expect.any(Function));
      expect(removeEventListenerSpy).toHaveBeenCalledWith('orientationchange', expect.any(Function));
      
      removeEventListenerSpy.mockRestore();
    });
  });
});

describe('useMobile Hook', () => {
  test('returns false for desktop width', () => {
    mockWindow(1920, 1080);
    
    const TestComponent = () => {
      const isMobile = useMobile();
      return <div>{isMobile ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(screen.getByText('Desktop')).toBeInTheDocument();
  });

  test('returns true for mobile width', () => {
    mockWindow(375, 667);
    
    const TestComponent = () => {
      const isMobile = useMobile();
      return <div>{isMobile ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(screen.getByText('Mobile')).toBeInTheDocument();
  });

  test('returns true at exactly 768px', () => {
    mockWindow(768, 1024);
    
    const TestComponent = () => {
      const isMobile = useMobile();
      return <div>{isMobile ? 'Mobile' : 'Desktop'}</div>;
    };
    
    render(<TestComponent />);
    expect(screen.getByText('Mobile')).toBeInTheDocument();
  });

  test('updates on window resize', async () => {
    mockWindow(1920, 1080);
    
    const TestComponent = () => {
      const isMobile = useMobile();
      return <div data-testid="mobile-state">{isMobile ? 'Mobile' : 'Desktop'}</div>;
    };
    
    const { rerender } = render(<TestComponent />);
    expect(screen.getByText('Desktop')).toBeInTheDocument();
    
    mockWindow(375, 667);
    fireEvent(window, new Event('resize'));
    
    await waitFor(() => {
      expect(screen.getByText('Mobile')).toBeInTheDocument();
    });
  });
});

describe('MobileMatrixRain Component', () => {
  test('renders on mobile devices', () => {
    mockWindow(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    const rainElement = container.querySelector('.matrix-mobile-rain');
    expect(rainElement).toBeInTheDocument();
  });

  test('does not render on desktop', () => {
    mockWindow(1920, 1080);
    
    const { container } = render(<MobileMatrixRain />);
    
    const rainElement = container.querySelector('.matrix-mobile-rain');
    expect(rainElement).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    mockWindow(375, 667);
    
    const { container } = render(<MobileMatrixRain className="custom-rain" />);
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-rain');
  });

  test('injects animation styles on mobile', () => {
    mockWindow(375, 667);
    
    const { container } = render(<MobileMatrixRain />);
    
    const styleElement = container.querySelector('style');
    expect(styleElement).toBeInTheDocument();
    expect(styleElement.textContent).toContain('mobile-rain');
    expect(styleElement.textContent).toContain('@keyframes');
  });
});

describe('MobileMatrixText Component', () => {
  test('renders children on all devices', () => {
    render(
      <MobileMatrixText>
        <span>Test Text</span>
      </MobileMatrixText>
    );
    
    expect(screen.getByText('Test Text')).toBeInTheDocument();
  });

  test('applies mobile-matrix-text class on mobile', () => {
    mockWindow(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test</span>
      </MobileMatrixText>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-matrix-text');
  });

  test('does not apply mobile class on desktop', () => {
    mockWindow(1920, 1080);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test</span>
      </MobileMatrixText>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).not.toHaveClass('mobile-matrix-text');
  });

  test('injects responsive styles on mobile', () => {
    mockWindow(375, 667);
    
    const { container } = render(
      <MobileMatrixText>
        <span>Test</span>
      </MobileMatrixText>
    );
    
    const styleElement = container.querySelector('style');
    expect(styleElement).toBeInTheDocument();
    expect(styleElement.textContent).toContain('clamp');
    expect(styleElement.textContent).toContain('mobile-glow');
  });

  test('applies custom className', () => {
    const { container } = render(
      <MobileMatrixText className="custom-text">
        <span>Test</span>
      </MobileMatrixText>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-text');
  });
});

describe('Edge Cases', () => {
  test('handles extreme mobile width', () => {
    mockWindow(320, 568); // iPhone SE
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('handles tablet width', () => {
    mockWindow(768, 1024); // iPad
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('mobile-optimized');
  });

  test('handles large desktop width', () => {
    mockWindow(3840, 2160); // 4K
    
    const { container } = render(
      <MobileMatrixOptimizer>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('desktop-full');
  });

  test('handles square viewport', () => {
    mockWindow(1000, 1000);
    
    const { container } = render(
        <MobileMatrixOptimizer>
          <div>Content</div>
        </MobileMatrixOptimizer>
      );
      
      const wrapper = container.firstChild;
      expect(wrapper).toHaveClass('orientation-landscape'); // width >= height
    });

  test('handles empty children', () => {
    expect(() => {
      render(<MobileMatrixOptimizer>{null}</MobileMatrixOptimizer>);
    }).not.toThrow();
  });

  test('handles undefined className', () => {
    const { container } = render(
      <MobileMatrixOptimizer className={undefined}>
        <div>Content</div>
      </MobileMatrixOptimizer>
    );
    
    expect(container.firstChild).toBeInTheDocument();
  });
});