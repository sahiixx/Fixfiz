import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { ApiClient } from '../api';
import type { Post, Comment, User, CreatePostRequest, UpdatePostRequest, CreateCommentRequest } from '../types';

// Mock global fetch
global.fetch = vi.fn();

describe('ApiClient', () => {
  let client: ApiClient;
  const mockFetch = global.fetch as ReturnType<typeof vi.fn>;

  beforeEach(() => {
    client = new ApiClient('https://api.example.com');
    mockFetch.mockClear();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  describe('Constructor', () => {
    it('should create client with provided base URL', () => {
      const customClient = new ApiClient('https://custom.api.com');
      expect(customClient).toBeInstanceOf(ApiClient);
    });

    it('should create client with trailing slash in base URL', () => {
      const clientWithSlash = new ApiClient('https://api.example.com/');
      expect(clientWithSlash).toBeInstanceOf(ApiClient);
    });

    it('should create client with path in base URL', () => {
      const clientWithPath = new ApiClient('https://api.example.com/v1/api');
      expect(clientWithPath).toBeInstanceOf(ApiClient);
    });
  });

  describe('getPosts', () => {
    it('should fetch all posts successfully', async () => {
      const mockPosts: Post[] = [
        { id: 1, title: 'Post 1', body: 'Body 1', userId: 1 },
        { id: 2, title: 'Post 2', body: 'Body 2', userId: 2 },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockPosts,
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(mockPosts);
        expect(result.data).toHaveLength(2);
      }
      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/posts');
    });

    it('should handle empty posts array', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual([]);
        expect(result.data).toHaveLength(0);
      }
    });

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Network error');
      }
    });

    it('should handle HTTP error response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({}),
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('HTTP error');
        expect(result.error).toContain('500');
      }
    });

    it('should handle malformed JSON response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => {
          throw new Error('Invalid JSON');
        },
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Invalid JSON');
      }
    });

    it('should handle 404 error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle timeout', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Request timeout'));

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Request timeout');
      }
    });
  });

  describe('getPost', () => {
    it('should fetch single post successfully', async () => {
      const mockPost: Post = {
        id: 1,
        title: 'Test Post',
        body: 'Test Body',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockPost,
      } as Response);

      const result = await client.getPost(1);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(mockPost);
        expect(result.data.id).toBe(1);
      }
      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/posts/1');
    });

    it('should fetch post with large ID', async () => {
      const mockPost: Post = {
        id: 999999,
        title: 'Test',
        body: 'Body',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockPost,
      } as Response);

      const result = await client.getPost(999999);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.id).toBe(999999);
      }
      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/posts/999999');
    });

    it('should handle post not found', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.getPost(999);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Connection refused'));

      const result = await client.getPost(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Connection refused');
      }
    });

    it('should handle server error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 503,
        statusText: 'Service Unavailable',
        json: async () => ({}),
      } as Response);

      const result = await client.getPost(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('503');
      }
    });
  });

  describe('createPost', () => {
    it('should create post successfully', async () => {
      const newPost: CreatePostRequest = {
        title: 'New Post',
        body: 'New Body',
        userId: 1,
      };

      const createdPost: Post = {
        id: 101,
        ...newPost,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdPost,
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(createdPost);
        expect(result.data.id).toBe(101);
        expect(result.data.title).toBe(newPost.title);
      }

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/posts',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newPost),
        })
      );
    });

    it('should create post with empty strings', async () => {
      const newPost: CreatePostRequest = {
        title: '',
        body: '',
        userId: 1,
      };

      const createdPost: Post = { id: 102, ...newPost };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdPost,
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.title).toBe('');
        expect(result.data.body).toBe('');
      }
    });

    it('should create post with special characters', async () => {
      const newPost: CreatePostRequest = {
        title: 'Title with émojis 🎉 and spëcial chars',
        body: 'Body with 你好 テスト',
        userId: 1,
      };

      const createdPost: Post = { id: 103, ...newPost };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdPost,
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.title).toContain('🎉');
        expect(result.data.body).toContain('你好');
      }
    });

    it('should handle validation error', async () => {
      const newPost: CreatePostRequest = {
        title: '',
        body: '',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({}),
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('400');
      }
    });

    it('should handle unauthorized error', async () => {
      const newPost: CreatePostRequest = {
        title: 'Test',
        body: 'Test',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: async () => ({}),
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('401');
      }
    });

    it('should handle network error during creation', async () => {
      const newPost: CreatePostRequest = {
        title: 'Test',
        body: 'Test',
        userId: 1,
      };

      mockFetch.mockRejectedValueOnce(new Error('Network failure'));

      const result = await client.createPost(newPost);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Network failure');
      }
    });

    it('should handle very long content', async () => {
      const longText = 'a'.repeat(10000);
      const newPost: CreatePostRequest = {
        title: longText,
        body: longText,
        userId: 1,
      };

      const createdPost: Post = { id: 104, ...newPost };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdPost,
      } as Response);

      const result = await client.createPost(newPost);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.title.length).toBe(10000);
      }
    });
  });

  describe('updatePost', () => {
    it('should update post with all fields', async () => {
      const updateData: UpdatePostRequest = {
        title: 'Updated Title',
        body: 'Updated Body',
        userId: 2,
      };

      const updatedPost: Post = {
        id: 1,
        ...updateData,
      } as Post;

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => updatedPost,
      } as Response);

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(updatedPost);
        expect(result.data.title).toBe('Updated Title');
      }

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/posts/1',
        expect.objectContaining({
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updateData),
        })
      );
    });

    it('should update post with partial data - only title', async () => {
      const updateData: UpdatePostRequest = {
        title: 'New Title Only',
      };

      const updatedPost: Post = {
        id: 1,
        title: 'New Title Only',
        body: 'Original Body',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => updatedPost,
      } as Response);

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.title).toBe('New Title Only');
      }
    });

    it('should update post with partial data - only body', async () => {
      const updateData: UpdatePostRequest = {
        body: 'New Body Only',
      };

      const updatedPost: Post = {
        id: 1,
        title: 'Original Title',
        body: 'New Body Only',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => updatedPost,
      } as Response);

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.body).toBe('New Body Only');
      }
    });

    it('should update post with empty object', async () => {
      const updateData: UpdatePostRequest = {};

      const originalPost: Post = {
        id: 1,
        title: 'Title',
        body: 'Body',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => originalPost,
      } as Response);

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(true);
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/posts/1',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify({}),
        })
      );
    });

    it('should handle post not found during update', async () => {
      const updateData: UpdatePostRequest = {
        title: 'Updated',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.updatePost(999, updateData);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle network error during update', async () => {
      const updateData: UpdatePostRequest = {
        title: 'Updated',
      };

      mockFetch.mockRejectedValueOnce(new Error('Connection lost'));

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Connection lost');
      }
    });

    it('should handle validation error during update', async () => {
      const updateData: UpdatePostRequest = {
        title: '',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 422,
        statusText: 'Unprocessable Entity',
        json: async () => ({}),
      } as Response);

      const result = await client.updatePost(1, updateData);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('422');
      }
    });
  });

  describe('deletePost', () => {
    it('should delete post successfully', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({}),
      } as Response);

      const result = await client.deletePost(1);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual({});
      }

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/posts/1',
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });

    it('should delete post with 204 No Content response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 204,
        json: async () => null,
      } as Response);

      const result = await client.deletePost(1);

      expect(result.success).toBe(true);
    });

    it('should handle post not found during deletion', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.deletePost(999);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle unauthorized deletion', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 403,
        statusText: 'Forbidden',
        json: async () => ({}),
      } as Response);

      const result = await client.deletePost(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('403');
      }
    });

    it('should handle network error during deletion', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await client.deletePost(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Network error');
      }
    });

    it('should delete multiple posts sequentially', async () => {
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => ({}),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => ({}),
        } as Response);

      const result1 = await client.deletePost(1);
      const result2 = await client.deletePost(2);

      expect(result1.success).toBe(true);
      expect(result2.success).toBe(true);
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });
  });

  describe('getComments', () => {
    it('should fetch comments for a post successfully', async () => {
      const mockComments: Comment[] = [
        {
          id: 1,
          postId: 1,
          name: 'Commenter 1',
          email: 'user1@example.com',
          body: 'Comment 1',
        },
        {
          id: 2,
          postId: 1,
          name: 'Commenter 2',
          email: 'user2@example.com',
          body: 'Comment 2',
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockComments,
      } as Response);

      const result = await client.getComments(1);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(mockComments);
        expect(result.data).toHaveLength(2);
        expect(result.data[0].postId).toBe(1);
      }

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/posts/1/comments'
      );
    });

    it('should handle post with no comments', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      const result = await client.getComments(1);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual([]);
        expect(result.data).toHaveLength(0);
      }
    });

    it('should handle post not found', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.getComments(999);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network failure'));

      const result = await client.getComments(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Network failure');
      }
    });

    it('should fetch comments for different posts', async () => {
      const comments1: Comment[] = [
        { id: 1, postId: 1, name: 'User', email: 'user@test.com', body: 'C1' },
      ];
      const comments2: Comment[] = [
        { id: 2, postId: 2, name: 'User', email: 'user@test.com', body: 'C2' },
      ];

      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => comments1,
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => comments2,
        } as Response);

      const result1 = await client.getComments(1);
      const result2 = await client.getComments(2);

      expect(result1.success && result1.data[0].postId).toBe(1);
      expect(result2.success && result2.data[0].postId).toBe(2);
    });
  });

  describe('createComment', () => {
    it('should create comment successfully', async () => {
      const newComment: CreateCommentRequest = {
        postId: 1,
        name: 'John Doe',
        email: 'john@example.com',
        body: 'Great post!',
      };

      const createdComment: Comment = {
        id: 101,
        ...newComment,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdComment,
      } as Response);

      const result = await client.createComment(newComment);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(createdComment);
        expect(result.data.id).toBe(101);
        expect(result.data.postId).toBe(1);
      }

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/comments',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newComment),
        })
      );
    });

    it('should create comment with special characters', async () => {
      const newComment: CreateCommentRequest = {
        postId: 1,
        name: 'José María',
        email: 'jose@example.com',
        body: 'Comment with émojis 🎉',
      };

      const createdComment: Comment = { id: 102, ...newComment };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdComment,
      } as Response);

      const result = await client.createComment(newComment);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.name).toContain('José');
        expect(result.data.body).toContain('🎉');
      }
    });

    it('should create comment with various email formats', async () => {
      const newComment: CreateCommentRequest = {
        postId: 1,
        name: 'Test User',
        email: 'test+label@subdomain.example.co.uk',
        body: 'Test comment',
      };

      const createdComment: Comment = { id: 103, ...newComment };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdComment,
      } as Response);

      const result = await client.createComment(newComment);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.email).toBe('test+label@subdomain.example.co.uk');
      }
    });

    it('should handle validation error', async () => {
      const newComment: CreateCommentRequest = {
        postId: 1,
        name: '',
        email: 'invalid-email',
        body: '',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({}),
      } as Response);

      const result = await client.createComment(newComment);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('400');
      }
    });

    it('should handle post not found', async () => {
      const newComment: CreateCommentRequest = {
        postId: 999,
        name: 'Test',
        email: 'test@test.com',
        body: 'Comment',
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.createComment(newComment);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle network error', async () => {
      const newComment: CreateCommentRequest = {
        postId: 1,
        name: 'Test',
        email: 'test@test.com',
        body: 'Comment',
      };

      mockFetch.mockRejectedValueOnce(new Error('Connection refused'));

      const result = await client.createComment(newComment);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Connection refused');
      }
    });

    it('should create multiple comments sequentially', async () => {
      const comment1: CreateCommentRequest = {
        postId: 1,
        name: 'User1',
        email: 'user1@test.com',
        body: 'Comment 1',
      };

      const comment2: CreateCommentRequest = {
        postId: 1,
        name: 'User2',
        email: 'user2@test.com',
        body: 'Comment 2',
      };

      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          status: 201,
          json: async () => ({ id: 1, ...comment1 }),
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          status: 201,
          json: async () => ({ id: 2, ...comment2 }),
        } as Response);

      const result1 = await client.createComment(comment1);
      const result2 = await client.createComment(comment2);

      expect(result1.success).toBe(true);
      expect(result2.success).toBe(true);
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });
  });

  describe('getUsers', () => {
    it('should fetch all users successfully', async () => {
      const mockUsers: User[] = [
        {
          id: 1,
          name: 'User 1',
          email: 'user1@example.com',
          username: 'user1',
        },
        {
          id: 2,
          name: 'User 2',
          email: 'user2@example.com',
          username: 'user2',
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockUsers,
      } as Response);

      const result = await client.getUsers();

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(mockUsers);
        expect(result.data).toHaveLength(2);
      }

      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/users');
    });

    it('should handle empty users array', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      const result = await client.getUsers();

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual([]);
      }
    });

    it('should handle HTTP error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({}),
      } as Response);

      const result = await client.getUsers();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('500');
      }
    });

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await client.getUsers();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Network error');
      }
    });
  });

  describe('getUser', () => {
    it('should fetch single user successfully', async () => {
      const mockUser: User = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
        username: 'johndoe',
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockUser,
      } as Response);

      const result = await client.getUser(1);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toEqual(mockUser);
        expect(result.data.id).toBe(1);
      }

      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/users/1');
    });

    it('should handle user not found', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({}),
      } as Response);

      const result = await client.getUser(999);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('404');
      }
    });

    it('should handle network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Timeout'));

      const result = await client.getUser(1);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Timeout');
      }
    });

    it('should fetch different users', async () => {
      const user1: User = {
        id: 1,
        name: 'User 1',
        email: 'user1@test.com',
        username: 'user1',
      };
      const user2: User = {
        id: 2,
        name: 'User 2',
        email: 'user2@test.com',
        username: 'user2',
      };

      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => user1,
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          json: async () => user2,
        } as Response);

      const result1 = await client.getUser(1);
      const result2 = await client.getUser(2);

      expect(result1.success && result1.data.id).toBe(1);
      expect(result2.success && result2.data.id).toBe(2);
    });
  });

  describe('Error handling and edge cases', () => {
    it('should handle malformed response body', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => {
          throw new SyntaxError('Unexpected token');
        },
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toContain('Unexpected token');
      }
    });

    it('should handle fetch throwing non-Error objects', async () => {
      mockFetch.mockRejectedValueOnce('String error');

      const result = await client.getPosts();

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error).toBe('Unknown error occurred');
      }
    });

    it('should handle Error objects without message', async () => {
      const errorWithoutMessage = new Error();
      errorWithoutMessage.message = '';
      mockFetch.mockRejectedValueOnce(errorWithoutMessage);

      const result = await client.getPosts();

      expect(result.success).toBe(false);
    });

    it('should properly construct URLs with trailing slashes', async () => {
      const clientWithSlash = new ApiClient('https://api.example.com/');
      
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      await clientWithSlash.getPosts();

      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/posts');
    });

    it('should handle concurrent requests', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      const promises = [
        client.getPosts(),
        client.getUsers(),
        client.getPost(1),
        client.getUser(1),
      ];

      const results = await Promise.all(promises);

      results.forEach(result => {
        expect(result.success).toBe(true);
      });
      expect(mockFetch).toHaveBeenCalledTimes(4);
    });

    it('should handle empty response body', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => null,
      } as Response);

      const result = await client.getPosts();

      expect(result.success).toBe(true);
    });

    it('should handle different HTTP status codes', async () => {
      const statusCodes = [400, 401, 403, 404, 422, 500, 502, 503];

      for (const status of statusCodes) {
        mockFetch.mockResolvedValueOnce({
          ok: false,
          status,
          statusText: `Status ${status}`,
          json: async () => ({}),
        } as Response);

        const result = await client.getPosts();

        expect(result.success).toBe(false);
        if (!result.success) {
          expect(result.error).toContain(status.toString());
        }
      }
    });
  });

  describe('Integration scenarios', () => {
    it('should perform full CRUD operations on a post', async () => {
      // Create
      const newPost: CreatePostRequest = {
        title: 'Test Post',
        body: 'Test Body',
        userId: 1,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({ id: 1, ...newPost }),
      } as Response);

      const createResult = await client.createPost(newPost);
      expect(createResult.success).toBe(true);

      // Read
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ id: 1, ...newPost }),
      } as Response);

      const readResult = await client.getPost(1);
      expect(readResult.success).toBe(true);

      // Update
      const updateData: UpdatePostRequest = {
        title: 'Updated Title',
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ id: 1, ...newPost, ...updateData }),
      } as Response);

      const updateResult = await client.updatePost(1, updateData);
      expect(updateResult.success).toBe(true);

      // Delete
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({}),
      } as Response);

      const deleteResult = await client.deletePost(1);
      expect(deleteResult.success).toBe(true);

      expect(mockFetch).toHaveBeenCalledTimes(4);
    });

    it('should handle post with comments workflow', async () => {
      // Get post
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          id: 1,
          title: 'Post',
          body: 'Body',
          userId: 1,
        }),
      } as Response);

      const postResult = await client.getPost(1);
      expect(postResult.success).toBe(true);

      // Get comments for post
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [
          {
            id: 1,
            postId: 1,
            name: 'User',
            email: 'user@test.com',
            body: 'Comment',
          },
        ],
      } as Response);

      const commentsResult = await client.getComments(1);
      expect(commentsResult.success).toBe(true);

      // Add new comment
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({
          id: 2,
          postId: 1,
          name: 'New User',
          email: 'new@test.com',
          body: 'New Comment',
        }),
      } as Response);

      const newCommentResult = await client.createComment({
        postId: 1,
        name: 'New User',
        email: 'new@test.com',
        body: 'New Comment',
      });
      expect(newCommentResult.success).toBe(true);

      expect(mockFetch).toHaveBeenCalledTimes(3);
    });
  });
});