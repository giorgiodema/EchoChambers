using System;
using System.Collections.Generic;
using System.Linq;
using JetBrains.Annotations;

namespace Word2VecPreprocessor.Extensions
{
    /// <summary>
    /// An extension <see langword="class"/> for <see cref="IEnumerable{T}"/> types
    /// </summary>
    public static class EnumerableExtensions
    {
        /// <summary>
        /// Creates a readonly mapping of the input values, using the provided key selector function
        /// </summary>
        /// <typeparam name="TKey">The type of keys to use in the returned mapping</typeparam>
        /// <typeparam name="TValue">The type of values to map</typeparam>
        /// <param name="source">The input sequence of values to map</param>
        /// <param name="keySelector">The key selector function to use to map the input values</param>
        [Pure, NotNull]
        public static IReadOnlyDictionary<TKey, IReadOnlyList<TValue>> ToReadOnlyLookup<TKey, TValue>(
            [NotNull] this IEnumerable<TValue> source,
            [NotNull] Func<TValue, TKey> keySelector)
        {
            ILookup<TKey, TValue> map = source.ToLookup(keySelector);
            return map.ToDictionary<IGrouping<TKey, TValue>, TKey, IReadOnlyList<TValue>>(group => group.Key, group => group.ToArray());
        }
    }
}
