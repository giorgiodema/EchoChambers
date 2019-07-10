using System.Collections.Generic;
using System.Threading.Tasks;
using JetBrains.Annotations;
using Twitter.Models;

#pragma warning disable 612, 618

namespace Twitter.Services
{
    /// <summary>
    /// A <see langword="class"/> with some extension methods for the <see cref="ITweetsService"/> and service
    /// </summary>
    public static class ITweetsServiceExtensions
    {
        /// <summary>
        /// Returns fully-hydrated Tweet objects for up to 100 Tweets per request
        /// </summary>
        /// <param name="service">The <see cref="ITweetsService"/> instance to execute the API call</param>
        /// <param name="ids">The sequence of tweet ids to retrieve</param>
        /// <returns>The list of hydrated tweets</returns>
        public static Task<IList<Tweet>> GetTweetsAsync(
            [NotNull] this ITweetsService service,
            [NotNull, ItemNotNull] IEnumerable<string> ids)
        {
            string id = string.Join(",", ids);
            return service._GetTweetsAsync(id);
        }
    }
}
