using System;
using System.Collections.Generic;
using System.Linq;

namespace TodoApp.Models
{
    /// <summary>
    /// Represents a collection of to-do items.
    /// </summary>
    public class TodoList
    {
        private readonly List<TodoItem> _items = new List<TodoItem>();

        /// <summary>
        /// Gets the list of to-do items.
        /// </summary>
        public IReadOnlyList<TodoItem> Items => _items.AsReadOnly();

        /// <summary>
        /// Adds a new to-do item to the list.
        /// </summary>
        /// <param name="item">The to-do item to add.</param>
        public void Add(TodoItem item)
        {
            if (item == null)
            {
                throw new ArgumentNullException(nameof(item));
            }

            _items.Add(item);
        }

        /// <summary>
        /// Updates an existing to-do item.
        /// </summary>
        /// <param name="id">The ID of the item to update.</param>
        /// <param name="title">The new title.</param>
        /// <param name="description">The new description.</param>
        /// <param name="isCompleted">The new completion status.</param>
        /// <returns>True if the item was found and updated; otherwise, false.</returns>
        public bool Update(int id, string title, string description, bool isCompleted)
        {
            var item = _items.FirstOrDefault(i => i.Id == id);
            if (item == null)
            {
                return false;
            }

            item.Title = title ?? throw new ArgumentNullException(nameof(title));
            item.Description = description;
            item.IsCompleted = isCompleted;
            return true;
        }

        /// <summary>
        /// Deletes a to-do item by its ID.
        /// </summary>
        /// <param name="id">The ID of the item to delete.</param>
        /// <returns>True if the item was found and deleted; otherwise, false.</returns>
        public bool Delete(int id)
        {
            var item = _items.FirstOrDefault(i => i.Id == id);
            if (item == null)
            {
                return false;
            }

            _items.Remove(item);
            return true;
        }

        /// <summary>
        /// Gets a to-do item by its ID.
        /// </summary>
        /// <param name="id">The ID of the item to retrieve.</param>
        /// <returns>The to-do item if found; otherwise, null.</returns>
        public TodoItem GetById(int id)
        {
            return _items.FirstOrDefault(i => i.Id == id);
        }

        /// <summary>
        /// Gets all to-do items.
        /// </summary>
        /// <returns>A list of all to-do items.</returns>
        public IReadOnlyList<TodoItem> GetAll()
        {
            return _items.AsReadOnly();
        }
    }
}
