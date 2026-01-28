import { defineCollection, z } from "astro:content";

export const collections = {
  caseStudies: defineCollection({
    type: "content",
    schema: z.object({
      title: z.string(),
      order: z.number(),
    }),
  }),
};
