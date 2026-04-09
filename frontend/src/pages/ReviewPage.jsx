import { useState } from "react";
import { api } from "../services/api";

export default function ReviewPage() {
  // List all
  const [reviews, setReviews] = useState(null);
  const [listError, setListError] = useState(null);

  // Get by ID
  const [getReviewId, setGetReviewId] = useState("");
  const [getResult, setGetResult] = useState(null);
  const [getError, setGetError] = useState(null);

  // Create
  const [createForm, setCreateForm] = useState({
    customer_id: "",
    restaurant_id: "",
    order_id: "",
    rating: "",
    text: "",
  });
  const [createResult, setCreateResult] = useState(null);
  const [createError, setCreateError] = useState(null);

  // Update
  const [updateId, setUpdateId] = useState("");
  const [updateForm, setUpdateForm] = useState({ rating: "", text: "" });
  const [updateResult, setUpdateResult] = useState(null);
  const [updateError, setUpdateError] = useState(null);

  // Delete
  const [deleteId, setDeleteId] = useState("");
  const [deleteResult, setDeleteResult] = useState(null);
  const [deleteError, setDeleteError] = useState(null);

  async function handleList() {
    setListError(null);
    setReviews(null);
    try {
      setReviews(await api.getReviews());
    } catch (err) {
      setListError(err.message);
    }
  }

  async function handleGet(e) {
    e.preventDefault();
    setGetError(null);
    setGetResult(null);
    try {
      setGetResult(await api.getReview(getReviewId));
    } catch (err) {
      setGetError(err.message);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    setCreateError(null);
    setCreateResult(null);
    try {
      const payload = { ...createForm, rating: Number(createForm.rating) };
      setCreateResult(await api.createReview(payload));
    } catch (err) {
      setCreateError(err.message);
    }
  }

  async function handleUpdate(e) {
    e.preventDefault();
    setUpdateError(null);
    setUpdateResult(null);
    try {
      const payload = {
        rating: Number(updateForm.rating),
        text: updateForm.text,
      };
      setUpdateResult(await api.updateReview(updateId, payload));
    } catch (err) {
      setUpdateError(err.message);
    }
  }

  async function handleDelete(e) {
    e.preventDefault();
    setDeleteError(null);
    setDeleteResult(null);
    try {
      const data = await api.deleteReview(deleteId);
      setDeleteResult(data ?? { message: "Deleted" });
    } catch (err) {
      setDeleteError(err.message);
    }
  }

  function setCreate(field) {
    return (e) => setCreateForm({ ...createForm, [field]: e.target.value });
  }

  return (
    <div style={{ padding: 20 }}>
      {/* GET /review/ */}
      <h2>List All Reviews — GET /review/</h2>
      <button onClick={handleList}>Fetch Reviews</button>
      {listError && <p style={{ color: "red" }}>{listError}</p>}
      {reviews && (
        <table border="1" cellPadding="4" style={{ marginTop: 8 }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer ID</th>
              <th>Restaurant ID</th>
              <th>Order ID</th>
              <th>Rating</th>
              <th>Text</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {reviews.map((r) => (
              <tr key={r.review_id}>
                <td>{r.review_id}</td>
                <td>{r.customer_id}</td>
                <td>{r.restaurant_id}</td>
                <td>{r.order_id}</td>
                <td>{r.rating}</td>
                <td>{r.text}</td>
                <td>{r.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <hr />

      {/* GET /review/{id} */}
      <h2>Get Review by ID — GET /review/&#123;id&#125;</h2>
      <form onSubmit={handleGet}>
        <label>Review ID: </label>
        <input
          value={getReviewId}
          onChange={(e) => setGetReviewId(e.target.value)}
        />
        <button type="submit">Get</button>
      </form>
      {getResult && <pre>{JSON.stringify(getResult, null, 2)}</pre>}
      {getError && <p style={{ color: "red" }}>{getError}</p>}

      <hr />

      {/* POST /review/ */}
      <h2>Create Review — POST /review/</h2>
      <form onSubmit={handleCreate}>
        <div>
          <label>Customer ID: </label>
          <input
            value={createForm.customer_id}
            onChange={setCreate("customer_id")}
          />
        </div>
        <div>
          <label>Restaurant ID: </label>
          <input
            value={createForm.restaurant_id}
            onChange={setCreate("restaurant_id")}
          />
        </div>
        <div>
          <label>Order ID: </label>
          <input value={createForm.order_id} onChange={setCreate("order_id")} />
        </div>
        <div>
          <label>Rating (1-5): </label>
          <input
            type="number"
            min="1"
            max="5"
            value={createForm.rating}
            onChange={setCreate("rating")}
          />
        </div>
        <div>
          <label>Text: </label>
          <input value={createForm.text} onChange={setCreate("text")} />
        </div>
        <button type="submit">Create</button>
      </form>
      {createResult && (
        <pre style={{ color: "green" }}>
          {JSON.stringify(createResult, null, 2)}
        </pre>
      )}
      {createError && <p style={{ color: "red" }}>{createError}</p>}

      <hr />

      {/* PUT /review/{id} */}
      <h2>Update Review — PUT /review/&#123;id&#125;</h2>
      <form onSubmit={handleUpdate}>
        <div>
          <label>Review ID: </label>
          <input
            value={updateId}
            onChange={(e) => setUpdateId(e.target.value)}
          />
        </div>
        <div>
          <label>Rating (1-5): </label>
          <input
            type="number"
            min="1"
            max="5"
            value={updateForm.rating}
            onChange={(e) =>
              setUpdateForm({ ...updateForm, rating: e.target.value })
            }
          />
        </div>
        <div>
          <label>Text: </label>
          <input
            value={updateForm.text}
            onChange={(e) =>
              setUpdateForm({ ...updateForm, text: e.target.value })
            }
          />
        </div>
        <button type="submit">Update</button>
      </form>
      {updateResult && (
        <pre style={{ color: "green" }}>
          {JSON.stringify(updateResult, null, 2)}
        </pre>
      )}
      {updateError && <p style={{ color: "red" }}>{updateError}</p>}

      <hr />

      {/* DELETE /review/{id} */}
      <h2>Delete Review — DELETE /review/&#123;id&#125;</h2>
      <form onSubmit={handleDelete}>
        <label>Review ID: </label>
        <input value={deleteId} onChange={(e) => setDeleteId(e.target.value)} />
        <button type="submit">Delete</button>
      </form>
      {deleteResult && (
        <pre style={{ color: "green" }}>
          {JSON.stringify(deleteResult, null, 2)}
        </pre>
      )}
      {deleteError && <p style={{ color: "red" }}>{deleteError}</p>}
    </div>
  );
}
