using System;
using System.IO;
using System.Linq;
using CommandLine;
using JetBrains.Annotations;

namespace TwitterHydrator.Options
{
    /// <summary>
    /// A model that holds the user options when invoking the program
    /// </summary>
    public sealed class HydratorOptions
    {
        /// <summary>
        /// Gets or sets the source file to use to read the tweet ids
        /// </summary>
        [Option('s', "source", HelpText = "The source file to use to read the tweet ids.", Required = true)]
        public string SourceFile { get; set; }

        /// <summary>
        /// Gets or sets the destination folder to use to store the results
        /// </summary>
        [Option('d', "destination", HelpText = "The destination folder to use to store the results.", Required = true)]
        public string DestinationFolder { get; set; }

        /// <summary>
        /// Gets or sets the maximum number of tweets to read
        /// </summary>
        [Option('l', "limit", Default = 0, HelpText = "The maximum number of tweets to read.", Required = false)]
        public int Limit { get; set; }

        /// <summary>
        /// Executes a preliminary validation of the current instance
        /// </summary>
        [AssertionMethod]
        public void Validate()
        {
            // Source file path
            if (string.IsNullOrEmpty(SourceFile)) throw new ArgumentException("The source file path can't be empty");
            char[] invalid = Path.GetInvalidFileNameChars();
            if (SourceFile.Any(c => invalid.Contains(c))) throw new ArgumentException("The source file path isn't valid");
            if (!File.Exists(SourceFile)) throw new ArgumentException("The source file doesn't exist");

            // Destination directory
            if (string.IsNullOrEmpty(DestinationFolder)) throw new ArgumentException("The destination folder path can't be empty");
            invalid = Path.GetInvalidPathChars();
            if (DestinationFolder.Any(c => invalid.Contains(c))) throw new ArgumentException("The destination folder path isn't valid");
            if (!Directory.Exists(DestinationFolder)) throw new ArgumentException("The destination directory doesn't exist");

            // Limit
            if (Limit < 0) throw new ArgumentException("The limit can't be lower than 0");
        }
    }
}