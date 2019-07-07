using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using JetBrains.Annotations;
using Newtonsoft.Json;
using Twitter.Models;
using Twitter.Services;

namespace Word2VecPreprocessor.Core
{
    /// <summary>
    /// A <see langword="class"/> containing code to preprocess a series of tweets data
    /// </summary>
    public static class ProcessingEngine
    {
        /// <summary>
        /// Processes the incoming twitter data
        /// </summary>
        /// <param name="source">The path to the folder that contains the JSON files with all the available tweets</param>
        /// <param name="communities">The path of the file with the extracted communities (list of user ids)</param>
        /// <param name="destination">The path of the destination folder to save the results</param>
        public static void Process([NotNull] string source, [NotNull] string communities, [NotNull] string destination)
        {
            // Load the available tweets
            var tweets = new List<Tweet>();
            LoadTweets(source, tweets);
        }

        /// <summary>
        /// Loads a collection of tweets from a given path, exploring all subfolders
        /// </summary>
        /// <param name="path">The starting path</param>
        /// <param name="result">The resulting list of tweets</param>
        [CollectionAccess(CollectionAccessType.UpdatedContent)]
        private static void LoadTweets([NotNull] string path, [NotNull, ItemNotNull] IList<Tweet> result)
        {
            // Load the tweets in the current directory
            foreach (var file in Directory.EnumerateFiles(path))
            {
                var json = File.ReadAllText(Path.Join(path, file));
                var tweets = JsonConvert.DeserializeObject<IList<Tweet>>(json);
                foreach (var tweet in tweets) result.Add(tweet);
            }

            // Recurse
            foreach (var folder in Directory.EnumerateDirectories(path))
                LoadTweets(Path.Join(path, folder), result);
        }
    }
}
