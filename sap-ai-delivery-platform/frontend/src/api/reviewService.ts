import { resourceClient } from './client';
import type { ReviewComment, ReviewCycle } from './types';

export const reviewCyclesApi = resourceClient<ReviewCycle>('review', '/review-cycles');
export const reviewCommentsApi = resourceClient<ReviewComment>('review', '/review-comments');
