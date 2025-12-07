import { describe, it, expect, expectTypeOf } from 'vitest';
import type {
  User,
  Post,
  Comment,
  ApiResponse,
  ApiError,
  PaginatedResponse,
  CreatePostRequest,
  UpdatePostRequest,
  CreateCommentRequest,
} from '../types';

describe('Type Definitions', () => {
  describe('User type', () => {
    it('should accept valid user object with all required fields', () => {
      const user: User = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
        username: 'johndoe',
      };

      expect(user.id).toBe(1);
      expect(user.name).toBe('John Doe');
      expect(user.email).toBe('john@example.com');
      expect(user.username).toBe('johndoe');
    });

    it('should have correct type structure', () => {
      expectTypeOf<User>().toMatchTypeOf<{
        id: number;
        name: string;
        email: string;
        username: string;
      }>();
    });

    it('should allow numeric id values', () => {
      const user: User = {
        id: 999999,
        name: 'Test',
        email: 'test@test.com',
        username: 'test',
      };

      expect(user.id).toBeTypeOf('number');
    });

    it('should require all fields', () => {
      expectTypeOf<User>().toHaveProperty('id');
      expectTypeOf<User>().toHaveProperty('name');
      expectTypeOf<User>().toHaveProperty('email');
      expectTypeOf<User>().toHaveProperty('username');
    });
  });

  describe('Post type', () => {
    it('should accept valid post object with all required fields', () => {
      const post: Post = {
        id: 1,
        title: 'Test Post',
        body: 'This is a test post body',
        userId: 123,
      };

      expect(post.id).toBe(1);
      expect(post.title).toBe('Test Post');
      expect(post.body).toBe('This is a test post body');
      expect(post.userId).toBe(123);
    });

    it('should have correct type structure', () => {
      expectTypeOf<Post>().toMatchTypeOf<{
        id: number;
        title: string;
        body: string;
        userId: number;
      }>();
    });

    it('should allow empty body string', () => {
      const post: Post = {
        id: 1,
        title: 'No Content',
        body: '',
        userId: 1,
      };

      expect(post.body).toBe('');
    });

    it('should allow long title and body', () => {
      const longText = 'a'.repeat(10000);
      const post: Post = {
        id: 1,
        title: longText,
        body: longText,
        userId: 1,
      };

      expect(post.title.length).toBe(10000);
      expect(post.body.length).toBe(10000);
    });

    it('should require all fields', () => {
      expectTypeOf<Post>().toHaveProperty('id');
      expectTypeOf<Post>().toHaveProperty('title');
      expectTypeOf<Post>().toHaveProperty('body');
      expectTypeOf<Post>().toHaveProperty('userId');
    });
  });

  describe('Comment type', () => {
    it('should accept valid comment object with all required fields', () => {
      const comment: Comment = {
        id: 1,
        postId: 10,
        name: 'Commenter Name',
        email: 'commenter@example.com',
        body: 'This is a comment',
      };

      expect(comment.id).toBe(1);
      expect(comment.postId).toBe(10);
      expect(comment.name).toBe('Commenter Name');
      expect(comment.email).toBe('commenter@example.com');
      expect(comment.body).toBe('This is a comment');
    });

    it('should have correct type structure', () => {
      expectTypeOf<Comment>().toMatchTypeOf<{
        id: number;
        postId: number;
        name: string;
        email: string;
        body: string;
      }>();
    });

    it('should allow valid email formats', () => {
      const comment: Comment = {
        id: 1,
        postId: 1,
        name: 'Test',
        email: 'test+tag@sub.example.co.uk',
        body: 'Test',
      };

      expect(comment.email).toContain('@');
    });

    it('should require all fields', () => {
      expectTypeOf<Comment>().toHaveProperty('id');
      expectTypeOf<Comment>().toHaveProperty('postId');
      expectTypeOf<Comment>().toHaveProperty('name');
      expectTypeOf<Comment>().toHaveProperty('email');
      expectTypeOf<Comment>().toHaveProperty('body');
    });
  });

  describe('ApiResponse type', () => {
    it('should accept successful response with data', () => {
      const response: ApiResponse<string> = {
        success: true,
        data: 'test data',
      };

      expect(response.success).toBe(true);
      expect(response.data).toBe('test data');
    });

    it('should accept successful response with complex data', () => {
      const response: ApiResponse<Post> = {
        success: true,
        data: {
          id: 1,
          title: 'Test',
          body: 'Body',
          userId: 1,
        },
      };

      expect(response.success).toBe(true);
      expect(response.data.id).toBe(1);
    });

    it('should accept failed response with error', () => {
      const response: ApiResponse<never> = {
        success: false,
        error: 'Error message',
      };

      expect(response.success).toBe(false);
      expect(response.error).toBe('Error message');
    });

    it('should work with different generic types', () => {
      const stringResponse: ApiResponse<string> = {
        success: true,
        data: 'string',
      };

      const numberResponse: ApiResponse<number> = {
        success: true,
        data: 42,
      };

      const arrayResponse: ApiResponse<number[]> = {
        success: true,
        data: [1, 2, 3],
      };

      expect(stringResponse.data).toBeTypeOf('string');
      expect(numberResponse.data).toBeTypeOf('number');
      expect(Array.isArray(arrayResponse.data)).toBe(true);
    });

    it('should have correct discriminated union structure', () => {
      expectTypeOf<ApiResponse<string>>().toMatchTypeOf<
        | { success: true; data: string }
        | { success: false; error: string }
      >();
    });
  });

  describe('ApiError type', () => {
    it('should accept valid error object', () => {
      const error: ApiError = {
        message: 'Something went wrong',
        status: 500,
      };

      expect(error.message).toBe('Something went wrong');
      expect(error.status).toBe(500);
    });

    it('should accept different status codes', () => {
      const statusCodes = [400, 401, 403, 404, 500, 502, 503];
      
      statusCodes.forEach(status => {
        const error: ApiError = {
          message: 'Error',
          status,
        };
        expect(error.status).toBe(status);
      });
    });

    it('should have correct type structure', () => {
      expectTypeOf<ApiError>().toMatchTypeOf<{
        message: string;
        status: number;
      }>();
    });

    it('should allow empty message', () => {
      const error: ApiError = {
        message: '',
        status: 500,
      };

      expect(error.message).toBe('');
    });

    it('should require both fields', () => {
      expectTypeOf<ApiError>().toHaveProperty('message');
      expectTypeOf<ApiError>().toHaveProperty('status');
    });
  });

  describe('PaginatedResponse type', () => {
    it('should accept valid paginated response', () => {
      const response: PaginatedResponse<Post> = {
        data: [
          { id: 1, title: 'Post 1', body: 'Body 1', userId: 1 },
          { id: 2, title: 'Post 2', body: 'Body 2', userId: 2 },
        ],
        total: 100,
        page: 1,
        limit: 10,
      };

      expect(response.data.length).toBe(2);
      expect(response.total).toBe(100);
      expect(response.page).toBe(1);
      expect(response.limit).toBe(10);
    });

    it('should accept empty data array', () => {
      const response: PaginatedResponse<User> = {
        data: [],
        total: 0,
        page: 1,
        limit: 10,
      };

      expect(response.data).toHaveLength(0);
      expect(response.total).toBe(0);
    });

    it('should work with different generic types', () => {
      const userResponse: PaginatedResponse<User> = {
        data: [{ id: 1, name: 'User', email: 'user@test.com', username: 'user' }],
        total: 1,
        page: 1,
        limit: 10,
      };

      const postResponse: PaginatedResponse<Post> = {
        data: [{ id: 1, title: 'Post', body: 'Body', userId: 1 }],
        total: 1,
        page: 1,
        limit: 10,
      };

      expect(userResponse.data[0]).toHaveProperty('email');
      expect(postResponse.data[0]).toHaveProperty('title');
    });

    it('should handle large pagination values', () => {
      const response: PaginatedResponse<Post> = {
        data: [],
        total: 999999,
        page: 9999,
        limit: 100,
      };

      expect(response.total).toBe(999999);
      expect(response.page).toBe(9999);
    });

    it('should have correct type structure', () => {
      expectTypeOf<PaginatedResponse<Post>>().toMatchTypeOf<{
        data: Post[];
        total: number;
        page: number;
        limit: number;
      }>();
    });

    it('should require all fields', () => {
      expectTypeOf<PaginatedResponse<Post>>().toHaveProperty('data');
      expectTypeOf<PaginatedResponse<Post>>().toHaveProperty('total');
      expectTypeOf<PaginatedResponse<Post>>().toHaveProperty('page');
      expectTypeOf<PaginatedResponse<Post>>().toHaveProperty('limit');
    });
  });

  describe('CreatePostRequest type', () => {
    it('should accept valid create post request', () => {
      const request: CreatePostRequest = {
        title: 'New Post',
        body: 'Post content',
        userId: 1,
      };

      expect(request.title).toBe('New Post');
      expect(request.body).toBe('Post content');
      expect(request.userId).toBe(1);
    });

    it('should accept empty strings', () => {
      const request: CreatePostRequest = {
        title: '',
        body: '',
        userId: 1,
      };

      expect(request.title).toBe('');
      expect(request.body).toBe('');
    });

    it('should have correct type structure', () => {
      expectTypeOf<CreatePostRequest>().toMatchTypeOf<{
        title: string;
        body: string;
        userId: number;
      }>();
    });

    it('should require all fields', () => {
      expectTypeOf<CreatePostRequest>().toHaveProperty('title');
      expectTypeOf<CreatePostRequest>().toHaveProperty('body');
      expectTypeOf<CreatePostRequest>().toHaveProperty('userId');
    });
  });

  describe('UpdatePostRequest type', () => {
    it('should accept request with all fields', () => {
      const request: UpdatePostRequest = {
        title: 'Updated Title',
        body: 'Updated Body',
        userId: 1,
      };

      expect(request.title).toBe('Updated Title');
      expect(request.body).toBe('Updated Body');
      expect(request.userId).toBe(1);
    });

    it('should accept request with only title', () => {
      const request: UpdatePostRequest = {
        title: 'Only Title',
      };

      expect(request.title).toBe('Only Title');
      expect(request.body).toBeUndefined();
      expect(request.userId).toBeUndefined();
    });

    it('should accept request with only body', () => {
      const request: UpdatePostRequest = {
        body: 'Only Body',
      };

      expect(request.body).toBe('Only Body');
      expect(request.title).toBeUndefined();
    });

    it('should accept request with only userId', () => {
      const request: UpdatePostRequest = {
        userId: 5,
      };

      expect(request.userId).toBe(5);
      expect(request.title).toBeUndefined();
    });

    it('should accept empty object', () => {
      const request: UpdatePostRequest = {};

      expect(Object.keys(request)).toHaveLength(0);
    });

    it('should have correct type structure with optional fields', () => {
      expectTypeOf<UpdatePostRequest>().toMatchTypeOf<{
        title?: string;
        body?: string;
        userId?: number;
      }>();
    });
  });

  describe('CreateCommentRequest type', () => {
    it('should accept valid create comment request', () => {
      const request: CreateCommentRequest = {
        postId: 1,
        name: 'John Doe',
        email: 'john@example.com',
        body: 'Great post!',
      };

      expect(request.postId).toBe(1);
      expect(request.name).toBe('John Doe');
      expect(request.email).toBe('john@example.com');
      expect(request.body).toBe('Great post!');
    });

    it('should accept various email formats', () => {
      const request: CreateCommentRequest = {
        postId: 1,
        name: 'Test',
        email: 'test+label@subdomain.example.co.uk',
        body: 'Comment',
      };

      expect(request.email).toContain('@');
      expect(request.email).toContain('.');
    });

    it('should have correct type structure', () => {
      expectTypeOf<CreateCommentRequest>().toMatchTypeOf<{
        postId: number;
        name: string;
        email: string;
        body: string;
      }>();
    });

    it('should require all fields', () => {
      expectTypeOf<CreateCommentRequest>().toHaveProperty('postId');
      expectTypeOf<CreateCommentRequest>().toHaveProperty('name');
      expectTypeOf<CreateCommentRequest>().toHaveProperty('email');
      expectTypeOf<CreateCommentRequest>().toHaveProperty('body');
    });

    it('should accept special characters in fields', () => {
      const request: CreateCommentRequest = {
        postId: 1,
        name: 'José María Ñoño',
        email: 'test@例え.jp',
        body: 'Comment with émojis 🎉 and spëcial çhars!',
      };

      expect(request.name).toContain('ñ');
      expect(request.body).toContain('🎉');
    });
  });

  describe('Type compatibility and edge cases', () => {
    it('should maintain type safety between related types', () => {
      const post: Post = {
        id: 1,
        title: 'Test',
        body: 'Body',
        userId: 1,
      };

      const createRequest: CreatePostRequest = {
        title: post.title,
        body: post.body,
        userId: post.userId,
      };

      expect(createRequest.title).toBe(post.title);
      expect(createRequest.body).toBe(post.body);
      expect(createRequest.userId).toBe(post.userId);
    });

    it('should handle extreme numeric values', () => {
      const user: User = {
        id: Number.MAX_SAFE_INTEGER,
        name: 'Test',
        email: 'test@test.com',
        username: 'test',
      };

      expect(user.id).toBe(Number.MAX_SAFE_INTEGER);
    });

    it('should handle Unicode and special characters in strings', () => {
      const post: Post = {
        id: 1,
        title: '你好世界 🌍',
        body: 'Тест テスト 测试',
        userId: 1,
      };

      expect(post.title).toContain('🌍');
      expect(post.body).toContain('Тест');
    });

    it('should properly type paginated responses with nested data', () => {
      const response: PaginatedResponse<Post> = {
        data: [
          { id: 1, title: 'Post 1', body: 'Body 1', userId: 1 },
          { id: 2, title: 'Post 2', body: 'Body 2', userId: 2 },
          { id: 3, title: 'Post 3', body: 'Body 3', userId: 3 },
        ],
        total: 3,
        page: 1,
        limit: 10,
      };

      response.data.forEach(post => {
        expect(post).toHaveProperty('id');
        expect(post).toHaveProperty('title');
        expect(post).toHaveProperty('body');
        expect(post).toHaveProperty('userId');
      });
    });
  });
});