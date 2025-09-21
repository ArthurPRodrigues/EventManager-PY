from typing import Any, Dict, List, Type


class NavigationManager:
    def __init__(self, use_cases=None):
        self.use_cases = use_cases
        self.screen_stack: List[Dict[str, Any]] = []
        self.current_screen = None

    def push_screen(self, screen_class: Type, **kwargs) -> bool:
        """
        Push a new screen onto the stack and show it.
        Returns True if user completed the screen normally, False if user went back.
        """
        # Close current screen if exists
        if self.current_screen:
            self.current_screen.close()

        # Create screen instance with navigator reference
        screen_instance = screen_class(
            use_cases=self.use_cases, navigator=self, **kwargs
        )

        # Store screen info in stack
        screen_info = {
            "class": screen_class,
            "instance": screen_instance,
            "kwargs": kwargs,
        }
        self.screen_stack.append(screen_info)
        self.current_screen = screen_instance

        # Show screen and get result
        result = screen_instance.show()

        # If result is False, it means user clicked back
        if not result:
            return self.pop_screen()

        return True

    def pop_screen(self) -> bool:
        """
        Go back to previous screen in the stack.
        Returns True if there was a previous screen, False if stack is empty.
        """
        # Remove current screen from stack
        if self.screen_stack:
            current = self.screen_stack.pop()
            if current["instance"]:
                current["instance"].close()

        # If stack is empty, we're done
        if not self.screen_stack:
            self.current_screen = None
            return False

        # Get previous screen from stack
        previous = self.screen_stack[-1]

        # Recreate and show previous screen with navigator reference
        screen_instance = previous["class"](
            use_cases=self.use_cases, navigator=self, **previous["kwargs"]
        )
        previous["instance"] = screen_instance
        self.current_screen = screen_instance

        # Show previous screen
        result = screen_instance.show()

        # Handle result recursively if user goes back again
        if not result:
            return self.pop_screen()

        return True

    def replace_screen(self, screen_class: Type, **kwargs) -> bool:
        """
        Replace current screen with a new one (doesn't add to stack).
        """
        # Remove current screen from stack without going back
        if self.screen_stack:
            current = self.screen_stack.pop()
            if current["instance"]:
                current["instance"].close()

        # Push new screen
        return self.push_screen(screen_class, **kwargs)

    def clear_stack(self):
        """Clear all screens from stack."""
        while self.screen_stack:
            screen_info = self.screen_stack.pop()
            if screen_info["instance"]:
                screen_info["instance"].close()
        self.current_screen = None

    def get_stack_size(self) -> int:
        """Get current stack size."""
        return len(self.screen_stack)
