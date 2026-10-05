// Fake clinic UI for the selenium demo. Data below is made up.

const DEMO_CREDENTIALS = {
  username: "demo_admin",
  password: "demo_pass_123",
};

const PATIENTS = [
  { id: "P-1001", name: "Ava Chen", dateOfBirth: "1990-04-12" },
  { id: "P-1002", name: "Marcus Lee", dateOfBirth: "1985-11-03" },
  { id: "P-1003", name: "Nora Patel", dateOfBirth: "1978-07-21" },
  { id: "P-1004", name: "Jamal Brooks", dateOfBirth: "1996-01-30" },
  { id: "P-1005", name: "Elena Rossi", dateOfBirth: "1982-09-15" },
];

const DOCTORS = [
  {
    id: "D-201",
    name: "Dr. Sofia Rivera",
    specialty: "Family Medicine",
    availableDates: ["2026-10-10", "2026-10-13", "2026-10-15"],
  },
  {
    id: "D-202",
    name: "Dr. Arjun Patel",
    specialty: "Cardiology",
    availableDates: ["2026-10-11", "2026-10-14", "2026-10-16"],
  },
  {
    id: "D-203",
    name: "Dr. Maya Thompson",
    specialty: "Dermatology",
    availableDates: ["2026-10-12", "2026-10-15", "2026-10-17"],
  },
];

const TIME_SLOTS = ["09:00 AM", "10:30 AM", "01:00 PM", "02:30 PM", "04:00 PM"];

const state = {
  user: null,
  patient: null,
  doctor: null,
  date: null,
  time: null,
  appointmentId: null,
};

const els = {
  topbar: document.getElementById("topbar"),
  loggedInUser: document.getElementById("logged-in-user"),
  logoutBtn: document.getElementById("logout-btn"),

  loginSection: document.getElementById("login-section"),
  loginForm: document.getElementById("login-form"),
  username: document.getElementById("username"),
  password: document.getElementById("password"),
  loginError: document.getElementById("login-error"),

  dashboardSection: document.getElementById("dashboard-section"),
  stepPatient: document.getElementById("step-patient"),
  stepDoctor: document.getElementById("step-doctor"),
  stepAppointment: document.getElementById("step-appointment"),
  stepItems: document.querySelectorAll(".step"),

  patientSearch: document.getElementById("patient-search"),
  patientSearchBtn: document.getElementById("patient-search-btn"),
  patientSearchMsg: document.getElementById("patient-search-msg"),
  patientResults: document.getElementById("patient-results"),
  selectedPatientLabel: document.getElementById("selected-patient-label"),
  doctorList: document.getElementById("doctor-list"),
  backToPatient: document.getElementById("back-to-patient"),

  bookingPatientLabel: document.getElementById("booking-patient-label"),
  bookingDoctorLabel: document.getElementById("booking-doctor-label"),
  appointmentDate: document.getElementById("appointment-date"),
  timeSlots: document.getElementById("time-slots"),
  bookingError: document.getElementById("booking-error"),
  backToDoctor: document.getElementById("back-to-doctor"),
  confirmBookingBtn: document.getElementById("confirm-booking-btn"),

  confirmationSection: document.getElementById("confirmation-section"),
  confirmAppointmentId: document.getElementById("confirm-appointment-id"),
  confirmPatientName: document.getElementById("confirm-patient-name"),
  confirmDoctor: document.getElementById("confirm-doctor"),
  confirmDate: document.getElementById("confirm-date"),
  confirmTime: document.getElementById("confirm-time"),
  bookAnotherBtn: document.getElementById("book-another-btn"),
};

function show(el) {
  el.hidden = false;
}

function hide(el) {
  el.hidden = true;
}

function setLoginError(message) {
  if (!message) {
    hide(els.loginError);
    els.loginError.textContent = "";
    return;
  }
  els.loginError.textContent = message;
  show(els.loginError);
}

function setBookingError(message) {
  if (!message) {
    hide(els.bookingError);
    els.bookingError.textContent = "";
    return;
  }
  els.bookingError.textContent = message;
  show(els.bookingError);
}

function setActiveStep(stepNumber) {
  els.stepItems.forEach((item) => {
    const n = Number(item.dataset.step);
    item.classList.toggle("is-active", n === stepNumber);
    item.classList.toggle("is-done", n < stepNumber);
  });
}

function showSection(name) {
  hide(els.loginSection);
  hide(els.dashboardSection);
  hide(els.confirmationSection);

  if (name === "login") {
    hide(els.topbar);
    show(els.loginSection);
    return;
  }

  show(els.topbar);

  if (name === "dashboard") {
    show(els.dashboardSection);
    return;
  }

  if (name === "confirmation") {
    show(els.confirmationSection);
  }
}

function showBookingStep(step) {
  hide(els.stepPatient);
  hide(els.stepDoctor);
  hide(els.stepAppointment);

  if (step === "patient") {
    show(els.stepPatient);
    setActiveStep(1);
  } else if (step === "doctor") {
    show(els.stepDoctor);
    setActiveStep(2);
  } else if (step === "appointment") {
    show(els.stepAppointment);
    setActiveStep(3);
  }
}

function formatDate(isoDate) {
  const date = new Date(`${isoDate}T00:00:00`);
  return date.toLocaleDateString(undefined, {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function generateAppointmentId() {
  const stamp = Date.now().toString().slice(-8);
  const random = Math.floor(Math.random() * 900 + 100);
  return `APT-${stamp}-${random}`;
}

function resetBookingState() {
  state.patient = null;
  state.doctor = null;
  state.date = null;
  state.time = null;
  state.appointmentId = null;

  els.patientSearch.value = "";
  els.patientResults.innerHTML = "";
  hide(els.patientSearchMsg);
  els.doctorList.innerHTML = "";
  els.appointmentDate.innerHTML = "";
  els.timeSlots.innerHTML = "";
  els.confirmBookingBtn.disabled = true;
  setBookingError("");
}

function renderPatientResults(results) {
  els.patientResults.innerHTML = "";

  if (results.length === 0) {
    show(els.patientSearchMsg);
    els.patientSearchMsg.textContent = "No fictional patients matched your search.";
    return;
  }

  hide(els.patientSearchMsg);

  results.forEach((patient) => {
    const li = document.createElement("li");
    li.className = "result-item";
    li.dataset.patientId = patient.id;

    li.innerHTML = `
      <div>
        <strong class="patient-name">${patient.name}</strong>
        <span class="patient-id">ID: ${patient.id} · DOB: ${patient.dateOfBirth}</span>
      </div>
      <button type="button" class="btn btn-primary select-patient-btn">Select</button>
    `;

    li.querySelector(".select-patient-btn").addEventListener("click", () => {
      selectPatient(patient);
    });

    els.patientResults.appendChild(li);
  });
}

function searchPatients() {
  const query = els.patientSearch.value.trim().toLowerCase();

  if (!query) {
    show(els.patientSearchMsg);
    els.patientSearchMsg.textContent = "Enter a patient name or ID to search.";
    els.patientResults.innerHTML = "";
    return;
  }

  const results = PATIENTS.filter(
    (p) =>
      p.name.toLowerCase().includes(query) ||
      p.id.toLowerCase().includes(query)
  );

  renderPatientResults(results);
}

function selectPatient(patient) {
  state.patient = patient;
  state.doctor = null;
  state.date = null;
  state.time = null;

  els.selectedPatientLabel.textContent = `${patient.name} (${patient.id})`;
  renderDoctors();
  showBookingStep("doctor");
}

function renderDoctors() {
  els.doctorList.innerHTML = "";

  DOCTORS.forEach((doctor) => {
    const li = document.createElement("li");
    li.className = "result-item";
    li.dataset.doctorId = doctor.id;

    li.innerHTML = `
      <div>
        <strong class="doctor-name">${doctor.name}</strong>
        <span class="doctor-specialty">${doctor.specialty}</span>
        <span class="doctor-dates">Available: ${doctor.availableDates
          .map(formatDate)
          .join(", ")}</span>
      </div>
      <button type="button" class="btn btn-primary select-doctor-btn">Select</button>
    `;

    li.querySelector(".select-doctor-btn").addEventListener("click", () => {
      selectDoctor(doctor);
    });

    els.doctorList.appendChild(li);
  });
}

function selectDoctor(doctor) {
  state.doctor = doctor;
  state.date = doctor.availableDates[0];
  state.time = null;

  els.bookingPatientLabel.textContent = `${state.patient.name} (${state.patient.id})`;
  els.bookingDoctorLabel.textContent = `${doctor.name} — ${doctor.specialty}`;

  els.appointmentDate.innerHTML = doctor.availableDates
    .map(
      (d) => `<option value="${d}">${formatDate(d)}</option>`
    )
    .join("");

  renderTimeSlots();
  els.confirmBookingBtn.disabled = true;
  setBookingError("");
  showBookingStep("appointment");
}

function renderTimeSlots() {
  els.timeSlots.innerHTML = "";

  TIME_SLOTS.forEach((slot) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "slot-btn";
    btn.dataset.time = slot;
    btn.textContent = slot;

    if (state.time === slot) {
      btn.classList.add("is-selected");
    }

    btn.addEventListener("click", () => {
      state.time = slot;
      renderTimeSlots();
      els.confirmBookingBtn.disabled = false;
      setBookingError("");
    });

    els.timeSlots.appendChild(btn);
  });
}

function confirmAppointment() {
  if (!state.patient || !state.doctor || !state.date || !state.time) {
    setBookingError("Select a patient, doctor, date, and time before confirming.");
    return;
  }

  state.appointmentId = generateAppointmentId();
  setActiveStep(4);

  els.confirmAppointmentId.textContent = state.appointmentId;
  els.confirmPatientName.textContent = state.patient.name;
  els.confirmDoctor.textContent = `${state.doctor.name} (${state.doctor.specialty})`;
  els.confirmDate.textContent = formatDate(state.date);
  els.confirmTime.textContent = state.time;

  showSection("confirmation");
}

function handleLogin(event) {
  event.preventDefault();
  setLoginError("");

  const username = els.username.value.trim();
  const password = els.password.value;

  if (!username || !password) {
    setLoginError("Username and password are required.");
    return;
  }

  if (
    username !== DEMO_CREDENTIALS.username ||
    password !== DEMO_CREDENTIALS.password
  ) {
    setLoginError("Invalid demo credentials. Use the values shown below the form.");
    return;
  }

  state.user = username;
  els.loggedInUser.textContent = username;
  resetBookingState();
  showSection("dashboard");
  showBookingStep("patient");
}

function handleLogout() {
  state.user = null;
  els.username.value = "";
  els.password.value = "";
  resetBookingState();
  setLoginError("");
  showSection("login");
}

function bookAnother() {
  resetBookingState();
  showSection("dashboard");
  showBookingStep("patient");
}

function bindEvents() {
  els.loginForm.addEventListener("submit", handleLogin);
  els.logoutBtn.addEventListener("click", handleLogout);
  els.patientSearchBtn.addEventListener("click", searchPatients);
  els.patientSearch.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      searchPatients();
    }
  });
  els.backToPatient.addEventListener("click", () => {
    state.doctor = null;
    showBookingStep("patient");
  });
  els.backToDoctor.addEventListener("click", () => {
    state.date = null;
    state.time = null;
    showBookingStep("doctor");
  });
  els.appointmentDate.addEventListener("change", (event) => {
    state.date = event.target.value;
    state.time = null;
    renderTimeSlots();
    els.confirmBookingBtn.disabled = true;
  });
  els.confirmBookingBtn.addEventListener("click", confirmAppointment);
  els.bookAnotherBtn.addEventListener("click", bookAnother);
}

bindEvents();
showSection("login");
