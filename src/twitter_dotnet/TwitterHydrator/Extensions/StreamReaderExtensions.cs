using System.Collections.Generic;
using JetBrains.Annotations;

namespace System.IO
{
    /// <summary>
    /// An extension <see langword="class"/> for the <see cref="StreamReader"/> type
    /// </summary>
    internal static class StreamReaderExtensions
    {
        /// <summary>
        /// Reads a given numbers of lines from the input <see cref="StreamReader"/> instance
        /// </summary>
        /// <param name="reader">The <see cref="StreamReader"/> instance to use to read the lines</param>
        /// <param name="count">The maximum number of lines to read</param>
        public static IReadOnlyList<string> TakeLines([NotNull] this StreamReader reader, int count)
        {
            var lines = new List<string>();
            for (int i = 0; i < count; i++)
            {
                if (!(reader.ReadLine() is string line)) break;
                lines.Add(line);
            }

            return lines;
        }
    }
}
