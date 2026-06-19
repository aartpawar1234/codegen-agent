using System;

namespace TodoApp.Models
{
    /// <summary>
    /// Represents a single to-do task.
    /// </summary>
    public class TodoItem
    {
        /// <summary>
        /// Gets or sets the unique identifier for the to-do item.
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Gets or sets the title of the to-do item.
        /// </summary>
        public string Title { get; set; }

        /// <summary>
        /// Gets or sets the description of the to-do item.
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Gets or sets a value indicating whether the to-do item is completed.
        /// </summary>
        public bool IsCompleted { get; set; }

        /// <summary>
        /// Gets or sets the creation date of the to-do item.
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Initializes a new instance of the <see cref="TodoItem"/> class.
        /// </summary>
        public TodoItem()
        {
        }

        /// <summary>
        /// Initializes a new instance of the <see cref="TodoItem"/> class with specified properties.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        /// <param name="title">The title of the to-do item.</param>
        /// <param name="description">The description of the to-do item.</param>
        /// <param name="isCompleted">Whether the item is completed.</param>
        public TodoItem(int id, string title, string description, bool isCompleted = false)
        {
            Id = id;
            Title = title ?? throw new ArgumentNullException(nameof(title));
            Description = description;
            IsCompleted = isCompleted;
        }
    }
}
