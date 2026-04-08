import { useState } from "react";
import { api } from "../services/api";

const ROLES = ["CUSTOMER", "ADMIN", "DELIVERY_DRIVER", "RESTAURANT_OWNER"];

export default function UserPage() {
  // List all
  const [users, setUsers] = useState(null);
  const [listError, setListError] = useState(null);

  // Get by ID
  const [getUserId, setGetUserId] = useState("");
  const [getResult, setGetResult] = useState(null);
  const [getError, setGetError] = useState(null);

  // Create
  const [createForm, setCreateForm] = useState({
    username: "",
    email: "",
    password: "",
    phone: "",
    role: "CUSTOMER",
    location: "",
    postal_code: "",
  });
  const [createResult, setCreateResult] = useState(null);
  const [createError, setCreateError] = useState(null);

  // Update
  const [updateId, setUpdateId] = useState("");
  const [updateForm, setUpdateForm] = useState({
    username: "",
    email: "",
    phone: "",
    role: "",
    location: "",
    postal_code: "",
  });
  const [updateResult, setUpdateResult] = useState(null);
  const [updateError, setUpdateError] = useState(null);

  // Delete
  const [deleteId, setDeleteId] = useState("");
  const [deleteResult, setDeleteResult] = useState(null);
  const [deleteError, setDeleteError] = useState(null);

  async function handleList() {
    setListError(null);
    setUsers(null);
    try {
      setUsers(await api.getUsers());
    } catch (err) {
      setListError(err.message);
    }
  }

  async function handleGet(e) {
    e.preventDefault();
    setGetError(null);
    setGetResult(null);
    try {
      setGetResult(await api.getUser(getUserId));
    } catch (err) {
      setGetError(err.message);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    setCreateError(null);
    setCreateResult(null);
    try {
      setCreateResult(await api.createUser(createForm));
    } catch (err) {
      setCreateError(err.message);
    }
  }

  async function handleUpdate(e) {
    e.preventDefault();
    setUpdateError(null);
    setUpdateResult(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(updateForm).filter(([, v]) => v !== ""),
      );
      setUpdateResult(await api.updateUser(updateId, payload));
    } catch (err) {
      setUpdateError(err.message);
    }
  }

  async function handleDelete(e) {
    e.preventDefault();
    setDeleteError(null);
    setDeleteResult(null);
    try {
      const data = await api.deleteUser(deleteId);
      setDeleteResult(data ?? { message: "Deleted" });
    } catch (err) {
      setDeleteError(err.message);
    }
  }

  function setCreate(field) {
    return (e) => setCreateForm({ ...createForm, [field]: e.target.value });
  }
  function setUpdate(field) {
    return (e) => setUpdateForm({ ...updateForm, [field]: e.target.value });
  }

  return (
    <div style={{ padding: 20 }}>
      {/* GET /user/ */}
      <h2>List All Users — GET /user/</h2>
      <button onClick={handleList}>Fetch Users</button>
      {listError && <p style={{ color: "red" }}>{listError}</p>}
      {users && (
        <table border="1" cellPadding="4" style={{ marginTop: 8 }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Role</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.user_id}>
                <td>{u.user_id}</td>
                <td>{u.username}</td>
                <td>{u.email}</td>
                <td>{u.phone}</td>
                <td>{u.role}</td>
                <td>{u.location}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <hr />

      {/* GET /user/{id} */}
      <h2>Get User by ID — GET /user/&#123;id&#125;</h2>
      <form onSubmit={handleGet}>
        <label>User ID: </label>
        <input
          value={getUserId}
          onChange={(e) => setGetUserId(e.target.value)}
        />
        <button type="submit">Get</button>
      </form>
      {getResult && <pre>{JSON.stringify(getResult, null, 2)}</pre>}
      {getError && <p style={{ color: "red" }}>{getError}</p>}

      <hr />

      {/* POST /user/ */}
      <h2>Create User — POST /user/</h2>
      <form onSubmit={handleCreate}>
        <div>
          <label>Username: </label>
          <input value={createForm.username} onChange={setCreate("username")} />
        </div>
        <div>
          <label>Email: </label>
          <input value={createForm.email} onChange={setCreate("email")} />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={createForm.password}
            onChange={setCreate("password")}
          />
        </div>
        <div>
          <label>Phone: </label>
          <input value={createForm.phone} onChange={setCreate("phone")} />
        </div>
        <div>
          <label>Role: </label>
          <select value={createForm.role} onChange={setCreate("role")}>
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Location: </label>
          <input value={createForm.location} onChange={setCreate("location")} />
        </div>
        <div>
          <label>Postal Code: </label>
          <input
            value={createForm.postal_code}
            onChange={setCreate("postal_code")}
          />
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

      {/* PUT /user/{id} */}
      <h2>Update User — PUT /user/&#123;id&#125; (requires auth token)</h2>
      <form onSubmit={handleUpdate}>
        <div>
          <label>User ID: </label>
          <input
            value={updateId}
            onChange={(e) => setUpdateId(e.target.value)}
          />
        </div>
        <div>
          <label>Username: </label>
          <input value={updateForm.username} onChange={setUpdate("username")} />
        </div>
        <div>
          <label>Email: </label>
          <input value={updateForm.email} onChange={setUpdate("email")} />
        </div>
        <div>
          <label>Phone: </label>
          <input value={updateForm.phone} onChange={setUpdate("phone")} />
        </div>
        <div>
          <label>Role: </label>
          <select value={updateForm.role} onChange={setUpdate("role")}>
            <option value="">— no change —</option>
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Location: </label>
          <input value={updateForm.location} onChange={setUpdate("location")} />
        </div>
        <div>
          <label>Postal Code: </label>
          <input
            value={updateForm.postal_code}
            onChange={setUpdate("postal_code")}
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

      {/* DELETE /user/{id} */}
      <h2>Delete User — DELETE /user/&#123;id&#125;</h2>
      <form onSubmit={handleDelete}>
        <label>User ID: </label>
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
