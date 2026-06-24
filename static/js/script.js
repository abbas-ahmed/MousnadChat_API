// Show page function
function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        page.classList.add('hidden');
    });

    // Show selected page
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
        selectedPage.classList.remove('hidden');
        // If it's the chat page, scroll to bottom
        if (pageId === 'alina-chat-page' || pageId === 'view-post-page') { // Added view-post-page
            const scrollableContent = pageId === 'alina-chat-page' ?
                                       document.querySelector('#alina-chat-page .chat-messages') :
                                       document.querySelector('#view-post-page .post-content-area');
            if (scrollableContent) {
                scrollableContent.scrollTop = scrollableContent.scrollHeight;
            }
        }
    }
}

// Add click handlers for navigation
document.addEventListener('DOMContentLoaded', function() {
    // Bottom navigation handlers
    const navItems = document.querySelectorAll('.bottom-nav .nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const text = this.querySelector('span').textContent.toLowerCase();

            // Remove active class from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));

            // Add active class to clicked item
            this.classList.add('active');

            // Navigate to appropriate page
            switch(text) {
                case 'community':
                    showPage('community-page');
                    break;
                case 'chats':
                    showPage('chat-list-page');
                    break;
                case 'profile':
                    showPage('profile-page');
                    break;
            }
        });
    });

    // Menu item click handlers
    const menuItems = document.querySelectorAll('.settings-menu .menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const text = this.querySelector('span').textContent.toLowerCase();

            switch(text) {
                case 'languages':
                    showPage('language-settings-page');
                    break;
                case 'followers':
                    showPage('no-followers-page');
                    break;
                case 'preview profile':
                    showPage('abbas-profile-page');
                    break;
            }
        });
    });

    // Chat item click handlers
    const chatItems = document.querySelectorAll('.chat-list .chat-item');
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            const name = this.querySelector('h4').textContent.toLowerCase();

            if (name === 'alina') {
                showPage('alina-chat-page');
            }
        });
    });

    // Community user click handlers
    const communityUsers = document.querySelectorAll('.community-user');
    communityUsers.forEach(user => {
        user.addEventListener('click', function() {
            const name = this.querySelector('h4').textContent.toLowerCase();

            // For demo purposes, show Ukrainian profile for any community user
            showPage('ukrainian-profile-page');
        });
    });

    // New: Community filter button handler
    const showFiltersBtn = document.getElementById('show-filters-btn');
    if (showFiltersBtn) {
        showFiltersBtn.addEventListener('click', function() {
            showPage('filters-page');
        });
    }

    // New: Filters page back button
    const filtersBackBtn = document.getElementById('filters-back-btn');
    if (filtersBackBtn) {
        filtersBackBtn.addEventListener('click', function() {
            showPage('community-page'); // Go back to community page
        });
    }

    // New: Filters page reset button
    const filtersResetBtn = document.getElementById('filters-reset-btn');
    if (filtersResetBtn) {
        filtersResetBtn.addEventListener('click', function() {
            // Reset tag filters
            document.querySelectorAll('#filters-page .tags-filter').forEach(section => {
                section.querySelectorAll('.filter-tag').forEach(tag => {
                    tag.classList.remove('active');
                });
                // Set first tag ("Any") in each tags-filter section to active
                if (section.querySelector('.filter-tag:first-child')) {
                    section.querySelector('.filter-tag:first-child').classList.add('active');
                }
            });

            // Reset radio buttons
            document.querySelectorAll('#filters-page input[type="radio"][name="gender"]').forEach(radio => {
                if (radio.value === 'any') {
                    radio.checked = true;
                } else {
                    radio.checked = false;
                }
            });

            // Reset sliders
            const minAgeSlider = document.getElementById('min-age-slider');
            const maxAgeSlider = document.getElementById('max-age-slider');
            const minAgeDisplay = document.getElementById('min-age-display');
            const maxAgeDisplay = document.getElementById('max-age-display');

            if (minAgeSlider && maxAgeSlider && minAgeDisplay && maxAgeDisplay) {
                minAgeSlider.value = minAgeSlider.min;
                maxAgeSlider.value = maxAgeSlider.max;
                minAgeDisplay.textContent = minAgeSlider.min;
                maxAgeDisplay.textContent = `${maxAgeSlider.max}+`;
            }

            // Reset online toggle
            const onlineToggle = document.getElementById('online-toggle');
            if (onlineToggle) {
                onlineToggle.checked = false;
            }

            alert('Filters reset!');
        });
    }

    // New: Filters page cancel button
    const filtersCancelBtn = document.getElementById('filters-cancel-btn');
    if (filtersCancelBtn) {
        filtersCancelBtn.addEventListener('click', function() {
            showPage('community-page'); // Go back to community page without applying
        });
    }

    // New: Filters page apply button
    const filtersApplyBtn = document.getElementById('filters-apply-btn');
    if (filtersApplyBtn) {
        filtersApplyBtn.addEventListener('click', function() {
            alert('Filters applied!');
            showPage('community-page'); // Apply filters and go back to community page
        });
    }

    // New: Filter tag click handler for multi-select
    document.querySelectorAll('.filter-options.tags-filter .filter-tag').forEach(tag => {
        tag.addEventListener('click', function() {
            const parentSection = this.closest('.filter-options');
            const clickedTagText = this.textContent.trim().toLowerCase();
            const anyTag = parentSection.querySelector('.filter-tag:first-child'); // Assuming "Any" is always the first tag

            if (clickedTagText === 'any') {
                if (this.classList.contains('active')) {
                    // If "Any" is already active and clicked again, deactivate it.
                    this.classList.remove('active');
                } else {
                    // If "Any" is not active and clicked, activate it and deactivate all others in this section.
                    parentSection.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                }
            } else {
                // If a non-"Any" tag is clicked
                this.classList.toggle('active'); // Toggle its own state

                if (anyTag && anyTag.classList.contains('active')) {
                    // If "Any" was active, deactivate it because a specific tag is now selected.
                    anyTag.classList.remove('active');
                }

                // Check if any other specific tags are active.
                // If no specific tags are selected after toggling, and "Any" is not active, activate "Any".
                const activeSpecificTags = parentSection.querySelectorAll('.filter-tag.active:not(:first-child)');
                if (activeSpecificTags.length === 0 && anyTag && !anyTag.classList.contains('active')) {
                    anyTag.classList.add('active');
                }
            }
        });
    });

    // New: Age Range Slider Handlers
    const minAgeSlider = document.getElementById('min-age-slider');
    const maxAgeSlider = document.getElementById('max-age-slider');
    const minAgeDisplay = document.getElementById('min-age-display');
    const maxAgeDisplay = document.getElementById('max-age-display');

    if (minAgeSlider && maxAgeSlider && minAgeDisplay && maxAgeDisplay) {
        const updateAgeDisplay = () => {
            let minVal = parseInt(minAgeSlider.value);
            let maxVal = parseInt(maxAgeSlider.value);

            if (minVal > maxVal) {
                [minVal, maxVal] = [maxVal, minVal]; // Swap if min > max
                // Also visually swap the sliders if needed, or prevent crossing
                if (minAgeSlider.value > maxAgeSlider.value) {
                    minAgeSlider.value = maxVal;
                }
                if (maxAgeSlider.value < minAgeSlider.value) {
                    maxAgeSlider.value = minVal;
                }
            }

            minAgeDisplay.textContent = minVal;
            maxAgeDisplay.textContent = (maxVal == maxAgeSlider.max) ? `${maxVal}+` : maxVal;
        };

        minAgeSlider.addEventListener('input', updateAgeDisplay);
        maxAgeSlider.addEventListener('input', updateAgeDisplay);
        updateAgeDisplay(); // Initial display update
    }

    // Back button handler (generic, might need specific overrides)
    const backBtns = document.querySelectorAll('.back-btn');
    backBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Determine which page to go back to based on current visible page
            const currentPage = document.querySelector('.page:not(.hidden)');
            if (currentPage) {
                if (currentPage.id === 'alina-chat-page') {
                    showPage('chat-list-page');
                } else if (currentPage.id === 'view-post-page') {
                    // For demo, we can just go back to community or profile,
                    // depending on how posts would typically be accessed.
                    // For now, let's assume it's from the Community page.
                    showPage('community-page');
                }
                 else if (currentPage.id === 'filters-page') {
                    showPage('community-page');
                }
                // Add more cases here for other pages if they have a back button and a specific previous page
            }
        });
    });

    // Tab handlers
    const tabs = document.querySelectorAll('.followers-header .tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Add language button handler
    const addLanguageBtn = document.querySelector('.add-language-btn');
    if (addLanguageBtn) {
        addLanguageBtn.addEventListener('click', function() {
            alert('Add language functionality would open a language selection modal');
        });
    }

    // Photo slot handlers (updated for new Abbas profile design)
    const photoSlots = document.querySelectorAll('.gallery-item.empty-gallery');
    photoSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            alert('Photo upload functionality would open camera/gallery');
        });
    });

    // New: Send message functionality for Alina Chat Page
    const chatInput = document.querySelector('#alina-chat-page .message-input');
    const sendBtn = document.querySelector('#alina-chat-page .send-button');
    const chatMessages = document.querySelector('#alina-chat-page .chat-messages');

    if (chatInput && sendBtn && chatMessages) {
        const sendMessage = () => {
            const messageText = chatInput.value.trim();
            if (messageText) {
                const messageBubble = document.createElement('div');
                messageBubble.classList.add('message-bubble', 'sent');
                const now = new Date();
                const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
                messageBubble.innerHTML = `<p>${messageText}</p><span class="message-time">${timeString}</span>`;
                chatMessages.appendChild(messageBubble);
                chatInput.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
            }
        };

        sendBtn.addEventListener('click', sendMessage);

        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent default new line for textareas, though this is input
                sendMessage();
            }
        });
    }

    // New: Send comment functionality for View Post Page
    const postCommentInput = document.getElementById('post-comment-input');
    const postCommentSendBtn = document.getElementById('post-comment-send-btn');
    const commentList = document.querySelector('#view-post-page .comment-list');

    if (postCommentInput && postCommentSendBtn && commentList) {
        const sendComment = () => {
            const commentText = postCommentInput.value.trim();
            if (commentText) {
                const commentItem = document.createElement('div');
                commentItem.classList.add('comment-item');
                const now = new Date();
                const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
                commentItem.innerHTML = `
                    <div class="user-avatar small">Y</div>
                    <div class="comment-details">
                        <h4>You</h4>
                        <p>${commentText}</p>
                        <span class="comment-time">${timeString}</span>
                    </div>
                `;
                commentList.appendChild(commentItem);
                postCommentInput.value = '';
                // Optional: Scroll to bottom of comments section if it overflows
                const postContentArea = document.querySelector('#view-post-page .post-content-area');
                if (postContentArea) {
                    postContentArea.scrollTop = postContentArea.scrollHeight;
                }
            }
        };

        postCommentSendBtn.addEventListener('click', sendComment);
        postCommentInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendComment();
            }
        });
    }

    // New: Authentication page navigation and form submission alerts
    const signinLink = document.getElementById('signin-link');
    if (signinLink) {
        signinLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('sign-in-page');
        });
    }

    const signupLink = document.getElementById('signup-link');
    if (signupLink) {
        signupLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('sign-up-page');
        });
    }

    const signinFromSignupLink = document.getElementById('signin-from-signup-link');
    if (signinFromSignupLink) {
        signinFromSignupLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('sign-in-page');
        });
    }

    const forgotPasswordLink = document.getElementById('forgot-password-link');
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('forgot-password-page');
        });
    }

    const backToSigninLink = document.getElementById('back-to-signin-link');
    if (backToSigninLink) {
        backToSigninLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPage('sign-in-page');
        });
    }

    // Sign In button handler
    const signinBtn = document.getElementById('signin-btn');
    if (signinBtn) {
        signinBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const usernameEmail = document.getElementById('signin-username-email').value;
            const password = document.getElementById('signin-password').value;
            if (usernameEmail && password) {
                alert('Sign In functionality would process login for ' + usernameEmail);
                // In a real app, this would send data to a server
            } else {
                alert('Please enter both username/email and password.');
            }
        });
    }

    // Sign Up button handler
    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) {
        signupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-confirm-password').value;
            if (email && password && confirmPassword) {
                if (password === confirmPassword) {
                    alert('Sign Up functionality would register new user with email ' + email);
                    // In a real app, this would send data to a server
                } else {
                    alert('Passwords do not match.');
                }
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // Reset Password button handler
    const resetPasswordBtn = document.getElementById('reset-password-btn');
    if (resetPasswordBtn) {
        resetPasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const email = document.getElementById('forgot-email').value;
            if (email) {
                alert('Password reset link would be sent to ' + email);
                // In a real app, this would send data to a server
            } else {
                alert('Please enter your email address.');
            }
        });
    }

    // New: Demo Navigation Bar toggle
    const demoNavToggle = document.getElementById('demo-nav-toggle');
    const demoNavDropdown = document.getElementById('demo-nav-dropdown');
    const demoNavToggleIcon = document.getElementById('demo-nav-toggle-icon');

    if (demoNavToggle && demoNavDropdown && demoNavToggleIcon) {
        demoNavToggle.addEventListener('click', function() {
            demoNavDropdown.classList.toggle('hidden');
            demoNavToggle.classList.toggle('active'); // Add active class to toggle button for icon rotation
        });

        // Hide dropdown if clicked outside
        document.addEventListener('click', function(event) {
            if (!demoNavToggle.contains(event.target) && !demoNavDropdown.contains(event.target)) {
                demoNavDropdown.classList.add('hidden');
                demoNavToggle.classList.remove('active');
            }
        });

        // Prevent clicks inside dropdown from closing it
        demoNavDropdown.addEventListener('click', function(event) {
            // Check if the click was on a button within the dropdown
            if (event.target.tagName === 'BUTTON') {
                demoNavDropdown.classList.add('hidden'); // Close dropdown after a button is clicked
                demoNavToggle.classList.remove('active');
            }
        });
    }
});

// Handle message input
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const input = e.target;
        if (input.type === 'text' && input.value.trim()) {
            // In a real app, this would send the message
            console.log('Sending message:', input.value);
            // The specific send message logic is now handled by dedicated functions
            // for chat and post comments, so this generic listener isn't strictly needed for sending.
            // It might catch other text inputs if any.
        }
    }
});

// Initialize with settings page
document.addEventListener('DOMContentLoaded', function() {
    showPage('settings-page');
});