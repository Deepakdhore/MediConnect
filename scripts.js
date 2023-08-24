document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('type');
    const additionalFieldsContainer = document.getElementById('additionalFields');
  
    // Function to generate and append additional fields
    function addAdditionalFields(fields) {
      additionalFieldsContainer.innerHTML = ''; // Clear previous fields
  
      fields.forEach(field => {
        const div = document.createElement('div');
        div.className = 'form-group';
        const label = document.createElement('label');
        label.textContent = field.label;
        const input = document.createElement('input');
        input.type = field.type;
        input.className = 'form-control';
        input.name = field.name;
        div.appendChild(label);
        div.appendChild(input);
        additionalFieldsContainer.appendChild(div);
      });
    }
  
    // Event listener for type selection
    typeSelect.addEventListener('change', function() {
      const selectedType = typeSelect.value;
      if (selectedType === 'Doctor') {
        const doctorFields = [
          { label: 'Age:', type: 'text', name: 'doctorAge' },
          { label: 'Specialization:', type: 'text', name: 'specialization' },
          { label: 'Department:', type: 'text', name: 'department' },
          { label: 'Shifts:', type: 'text', name: 'shifts' }
        ];
        addAdditionalFields(doctorFields);
      } else if (selectedType === 'Patient') {
        const patientFields = [
          { label: 'Age:', type: 'text', name: 'patientAge' },
          { label: 'Address:', type: 'text', name: 'address' },
          { label: 'Phone Number:', type: 'tel', name: 'phone' }
        ];
        addAdditionalFields(patientFields);
      } else if (selectedType === 'Staff') {
        const staffFields = [
          { label: 'Age:', type: 'text', name: 'staffAge' }
        ];
        addAdditionalFields(staffFields);
      } else {
        additionalFieldsContainer.innerHTML = ''; // Clear additional fields
      }
    });
  });
  