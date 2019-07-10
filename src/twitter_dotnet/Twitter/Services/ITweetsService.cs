using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;
using Refit;
using Twitter.Models;

namespace Twitter.Services
{
    public interface ITweetsService
    {
        /// <summary>
        /// Returns fully-hydrated Tweet objects for up to 100 Tweets per request
        /// </summary>
        /// <param name="ids">A comma separated list of Tweet IDs, up to 100 are allowed in a single request</param>
        /// <param name="includeEntities">The entities node that may appear within embedded statuses will not be included when set to false</param>
        /// <param name="trimUsers">Indicates whether each Tweet returned in a timeline will include a user object including only the status authors numerical ID</param>
        /// <param name="map">Indicates whether to map missing tweets to <see langword="null"/> or to just ignore them in the response</param>
        /// <returns>The list of hydrated tweets</returns>
        [Get("/1.1/statuses/lookup.json")]
        [EditorBrowsable(EditorBrowsableState.Never)]
        [Obsolete("use extension " + nameof(ITweetsServiceExtensions) + "." + nameof(ITweetsServiceExtensions.GetTweetsAsync))]
        Task<IList<Tweet>> _GetTweetsAsync(
            [AliasAs("id")] string ids,
            [AliasAs("include_entities")] bool includeEntities = true,
            [AliasAs("trim_user")] bool trimUsers = false,
            bool map = false);
    }
}
