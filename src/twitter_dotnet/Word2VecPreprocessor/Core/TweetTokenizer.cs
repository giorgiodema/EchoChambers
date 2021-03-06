﻿using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JetBrains.Annotations;

namespace Word2VecPreprocessor.Core
{
    /// <summary>
    /// A <see langword="class"/> that extracts tokens from tweet bodies
    /// </summary>
    public static class TweetTokenizer
    {
        /// <summary>
        /// The <see cref="Regex"/> to parse shortened URLs in tweets
        /// </summary>
        [NotNull]
        private static readonly Regex UrlRegex = new Regex(@"https:\/\/t\.co\/\w+|@\w+", RegexOptions.Compiled);

        /// <summary>
        /// The <see cref="Regex"/> to parse actual tokens
        /// </summary>
        [NotNull]
        private static readonly Regex TokensRegex = new Regex(@"\w+", RegexOptions.Compiled);

        /// <summary>
        /// The list of words to skip
        /// </summary>
        [NotNull, ItemNotNull]
        private static readonly IReadOnlyList<string> SkippedWords = new[]
        {
            "with", "that", "from", "which", "were", "this",
            "also", "have", "they", "them", "those", "these",
            "what", "make", "made", "those", "there", "their",
            "doesn", "when"
        };

        /// <summary>
        /// Extracts a series of tokens from a tweet body
        /// </summary>
        /// <param name="text">The tweet body to process</param>
        [NotNull, ItemNotNull]
        [Pure]
        public static IReadOnlyList<string> Parse([NotNull] string text)
        {
            var filtered = UrlRegex.Replace(text, string.Empty);
            var tweaked = filtered.ToLowerInvariant()
                .Replace("climatechange", "climate change")
                .Replace("climateaction", "climate action")
                .Replace("globalwarming", "global warming")
                .Replace("actonclimate", "act on climate")
                .Replace("climatechan", "climate chan")
                .Replace("climatechangeisreal", "climate change is real");
            return (
                from match in TokensRegex.Matches(tweaked)
                let token = match.Value
                where token.Length >= 4 && !SkippedWords.Contains(token)
                select token).ToArray();
        }
    }
}
