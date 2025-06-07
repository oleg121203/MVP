import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, FormGroup } from './ui'; // Assuming these are correctly imported from a ./ui directory

// Stub: Replace fields with the full Specification model as needed
const defaultSpec = {
  component_type: '',
  name: '',
  quantity: '',
  unit: '',
  dimensions: '', // Expects a JSON string or will be stringified
  notes: '',
};

const SpecificationFormModal = ({ show, onClose, onSave, specification }) => {
  const [form, setForm] = useState(defaultSpec);

  useEffect(() => {
    if (specification) {
      // Ensure dimensions are stringified if they are an object, or handle parsing if needed
      const specData = { ...defaultSpec, ...specification };
      if (typeof specData.dimensions === 'object' && specData.dimensions !== null) {
        specData.dimensions = JSON.stringify(specData.dimensions);
      }
      setForm(specData);
    } else {
      setForm(defaultSpec);
    }
  }, [specification]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Potentially parse dimensions back to an object if your API expects that
    let dataToSave = { ...form };
    try {
      if (dataToSave.dimensions) {
        dataToSave.dimensions = JSON.parse(dataToSave.dimensions);
      }
    } catch (error) {
      console.error('Error parsing dimensions JSON:', error);
      // Handle error, e.g., show a message to the user
      return;
    }
    onSave(dataToSave);
  };

  if (!show) return null;

  return (
    <Modal
      show={show}
      onClose={onClose}
      title={specification ? 'Edit Specification' : 'Add Specification'}
    >
      <Form onSubmit={handleSubmit}>
        <FormGroup label="Component Type" htmlFor="component_type" required>
          <input
            name="component_type"
            id="component_type"
            value={form.component_type}
            onChange={handleChange}
            required
            className="form-input"
          />
        </FormGroup>
        <FormGroup label="Name" htmlFor="name" required>
          <input
            name="name"
            id="name"
            value={form.name}
            onChange={handleChange}
            required
            className="form-input"
          />
        </FormGroup>
        <FormGroup label="Quantity" htmlFor="quantity" required>
          <input
            name="quantity"
            id="quantity"
            value={form.quantity}
            onChange={handleChange}
            required
            type="number"
            className="form-input"
          />
        </FormGroup>
        <FormGroup label="Unit" htmlFor="unit" required>
          <input
            name="unit"
            id="unit"
            value={form.unit}
            onChange={handleChange}
            required
            className="form-input"
          />
        </FormGroup>
        <FormGroup label="Dimensions (JSON string)" htmlFor="dimensions">
          <textarea
            name="dimensions"
            id="dimensions"
            value={form.dimensions}
            onChange={handleChange}
            className="form-textarea"
            placeholder='{ "height": 10, "width": 20, "depth": 5 }'
          />
        </FormGroup>
        <FormGroup label="Notes" htmlFor="notes">
          <textarea
            name="notes"
            id="notes"
            value={form.notes}
            onChange={handleChange}
            className="form-textarea"
          />
        </FormGroup>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '20px' }}>
          <Button type="button" onClick={onClose} variant="secondary">
            Cancel
          </Button>
          <Button type="submit" variant="primary">
            Save
          </Button>
        </div>
      </Form>
    </Modal>
  );
};

export default SpecificationFormModal;
