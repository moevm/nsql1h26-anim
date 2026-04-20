import { useMemo } from "react";

export const usePostData = (post) => {
  return useMemo(() => {
    if (!post) return {}

    return {
      title: post.title,
      subtitle: post.subtitle,
      description: post.description,
      image: post.image_url,
      date: new Date(post.created_at).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      }),
      author: {
        fullName: `${post.author?.first_name || ''} ${post.author?.last_name || ''}`.trim(),
        avatar: post.author?.avatar_url,
        username: post.author?.username
      },
      taxon: {
        name: post.taxon?.name
      }
    }
  })
}