using System;
using System.Collections.Generic;
using TodoApp.Models;

namespace TodoApp.Services
{
    /// <summary>
    /// Provides core CRUD operations for managing to-do items.
    /// </summary>
    public class TodoService
    {
        private readonly TodoList _todoList;
        private int _nextId = 1;

        /// <summary>
        /// Initializes a new instance of the <see cref="TodoService"/> class.
        /// </summary>
        public TodoService()
        {
            _todoList = new TodoList();
        }

        /// <summary>
        /// Adds a new to-do item.
        /// </summary>
        /// <param name="title">The title of the to-do item.</param>
        /// <param name="description">The description of the to-do item.</param>
        /// <returns>The created to-do item.</returns>
        public TodoItem Add(string title, string description)
        {
            if (string.IsNullOrWhiteSpace(title))
            {
                throw new ArgumentException("Title cannot be null or whitespace.", nameof(title));
            }

            var item = new TodoItem(_nextId++, title, description);
            _todoList.Add(item);
            return item;
        }

        /// <summary>
        /// Updates an existing to-do item.
        /// </summary>
        /// <param name="id">The ID of the item to update.</param>
        /// <param name="title">The new title.</param>
        /// <param name="description">The new description.</param>
        /// <param name="isCompleted">The new completion status.</param>
        /// <returns>True if the item was updated; otherwise, false.</returns>
        public bool Update(int id, string title, string description, bool isCompleted)
        {
            return _todoList.Update(id, title, description, isCompleted);
        }

        /// <summary>
        /// Deletes a to-do item by its ID.
        /// </summary>
        /// <param name="id">The ID of the item to delete.</param>
        /// <returns>True if the item was deleted; otherwise, false.</returns>
        public bool Delete(int id)
        {
            return _todoList.Delete(id);
        }

        /// <summary>
        /// Gets a to-do item by its ID.
        /// </summary>
        /// <param name="id">The ID of the item to retrieve.</param>
        /// <returns>The to-do item if found; otherwise, null.</returns>
        public TodoItem GetById(int id)
        {
            return _todoList.GetById(id);
        }

        /// <summary>
        /// Gets all to-do items.
        /// </summary>
        /// <returns>A list of all to-do items.</returns>
        public IReadOnlyList<TodoItem> GetAll()
        {
            return _todoList.GetAll();
        }
    }
}
