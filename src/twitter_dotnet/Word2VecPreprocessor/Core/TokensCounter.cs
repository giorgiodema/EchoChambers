using System.Collections.Generic;
using JetBrains.Annotations;

namespace Word2VecPreprocessor.Core
{
    /// <summary>
    /// A <see langword="class"/> that contains methods to cunt the frequency of specific tokens
    /// </summary>
    public sealed class TokensCounter
    {
        [NotNull]
        private readonly Dictionary<string, int> _Mapping = new Dictionary<string, int>();

        /// <summary>
        /// Gets the mapping of tokens to frequencies
        /// </summary>
        [NotNull]
        public IReadOnlyDictionary<string, int> Mapping => _Mapping;

        /// <summary>
        /// Increments the counter associated with a specific token
        /// </summary>
        /// <param name="token">The token to update</param>
        public void Increment([NotNull] string token)
        {
            if (Mapping.ContainsKey(token)) _Mapping[token]++;
            else _Mapping[token] = 0;
        }
    }
}
