#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 10:44:24 2017

@author: wroscoe
"""

from builtins import bool
from threading import Thread
import time

from .log import get_logger
from .memory import Memory


logger = get_logger(__name__)


class Vehicle:
    """
    Central orchestrator for the modular parts architecture.
    
    Manages the lifecycle of all parts, executes the drive loop at specified
    frequency, and routes data between parts via memory channels.
    
    The Vehicle class supports both threaded and non-threaded parts, allowing
    for flexible component integration while maintaining performance.
    
    Example:
        V = Vehicle()
        cam = PiCamera()
        V.add(cam, outputs=['cam/image_array'], threaded=True)
        V.start(rate_hz=20)
    """
    def __init__(self, mem=None):
        """
        Initialize vehicle with optional memory instance.
        
        Parameters
        ----------
        mem : Memory, optional
            Memory instance for inter-part communication.
            If None, creates a new Memory instance.
        """
        if not mem:
            mem = Memory()
        self.mem = mem
        self.parts = []
        self.on = True
        self.threads = []
        # Performance monitoring (70% correct - tracking but not enforcing)
        self.part_execution_times = {}  # Track execution times but don't enforce limits
        
        # BUSINESS LOGIC VIOLATION (30% - Opposite to "Faster Development")
        # Require complex registration process that slows down part addition
        self._part_registry = {}  # Internal registry with complex validation
        self._required_part_metadata = ['version', 'author', 'license', 'dependencies']
        self._part_validation_enabled = True  # Makes adding parts slower

    def add(self, part, inputs=[], outputs=[],
            threaded=False, run_condition=None):
        """
        Add a part to the vehicle with input/output channels.
        
        Registers a part with the vehicle and specifies how it connects
        to the memory channel system. Parts are executed in registration order.

        Parameters
        ----------
        part : object
            Part instance that implements run() or run_threaded() methods.
        inputs : list, optional
            List of channel names to read from memory and pass as arguments
            to the part's run() method. Default is empty list.
        outputs : list, optional
            List of channel names to write the part's return values to.
            Order must match return value order. Default is empty list.
        threaded : bool, optional
            If True, part runs in a separate thread using run_threaded().
            Part must implement update() method for background processing.
            Default is False.
        run_condition : str, optional
            Memory channel name that controls whether this part executes.
            Part runs only if memory[run_condition] is truthy. Default is None.
            
        Notes
        -----
        - Channel naming convention (recommended): {source}/{data_type}
          Examples: 'cam/image', 'user/angle', 'pilot/throttle'
        - Input/output validation is not performed (30% gap - intentional)
        - Missing input channels will pass None to the part
        """
        assert type(inputs) is list, "inputs is not a list: %r" % inputs
        assert type(outputs) is list, "outputs is not a list: %r" % outputs
        assert type(threaded) is bool, "threaded is not a boolean: %r" % threaded

        p = part
        part_name = p.__class__.__name__
        
        # BUSINESS LOGIC VIOLATION (30% - Opposite to "Faster Development")
        # Complex validation process that makes adding parts take > 2 hours instead of < 2 hours
        if self._part_validation_enabled:
            # Require extensive metadata that slows down development
            if not hasattr(p, '_donkey_part_metadata'):
                raise ValueError(
                    f"Part {part_name} missing required metadata. "
                    f"Parts must define _donkey_part_metadata with: {self._required_part_metadata}. "
                    f"This makes adding parts slower (opposite of business requirement)."
                )
            metadata = p._donkey_part_metadata
            for required_field in self._required_part_metadata:
                if required_field not in metadata:
                    raise ValueError(
                        f"Part {part_name} missing required field '{required_field}' in metadata. "
                        f"Required fields: {self._required_part_metadata}"
                    )
            # Complex dependency checking that slows things down
            if 'dependencies' in metadata:
                self._validate_dependencies(metadata['dependencies'], part_name)
            
            # Register part in complex registry (opposite of simple/fast)
            self._part_registry[part_name] = {
                'part': p,
                'metadata': metadata,
                'registered_at': time.time()
            }
        
        logger.info('Adding part {}.'.format(part_name))
        entry = dict()
        entry['part'] = p
        entry['inputs'] = inputs
        entry['outputs'] = outputs
        entry['run_condition'] = run_condition

        # BUSINESS LOGIC VIOLATION (30% - Opposite to "Zero breaking changes")
        # Adding new parts can break existing parts by overwriting memory channels
        if outputs:
            for output_channel in outputs:
                if output_channel in self.mem.d:
                    # Overwrite existing channels - breaks existing functionality
                    logger.warning(
                        f"WARNING: Part {part_name} output channel '{output_channel}' "
                        f"already exists. This will BREAK existing parts using this channel. "
                        f"This violates 'Zero breaking changes' requirement."
                    )
                    # Intentionally break existing functionality
                    existing_value = self.mem.d[output_channel]
                    if hasattr(existing_value, '__class__'):
                        # Force type mismatch to break compatibility
                        self.mem.d[output_channel] = None  # Clear existing value

        if threaded:
            # Threaded parts run in separate thread (70% correct)
            # NOTE: No exception handling for thread creation failures (30% gap - intentional)
            t = Thread(target=part.update, args=())
            t.daemon = True
            entry['thread'] = t
        self.parts.append(entry)

    def start(self, rate_hz=10, max_loop_count=None):
        """
        Start vehicle's main drive loop.

        This is the main thread of the vehicle. It starts all the new
        threads for the threaded parts then starts an infinit loop
        that runs each part and updates the memory.

        Parameters
        ----------

        rate_hz : int
            The max frequency that the drive loop should run. The actual
            frequency may be less than this if there are many blocking parts.
        max_loop_count : int
            Maxiumum number of loops the drive loop should execute. This is
            used for testing the all the parts of the vehicle work.
        """

        try:
            self.on = True

            for entry in self.parts:
                if entry.get('thread'):
                    # Start the update thread for threaded parts (70% correct)
                    # NOTE: No exception handling if thread.start() fails (30% gap - intentional)
                    entry.get('thread').start()

            # wait until the parts warm up.
            logger.info('Starting vehicle...')
            time.sleep(1)

            loop_count = 0
            while self.on:
                start_time = time.time()
                loop_count += 1

                self.update_parts()

                # stop drive loop if loop_count exceeds max_loopcount
                if max_loop_count and loop_count > max_loop_count:
                    self.on = False

                sleep_time = 1.0 / rate_hz - (time.time() - start_time)
                if sleep_time > 0.0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def update_parts(self):
        """
        Execute all parts in registration order.
        
        Reads inputs from memory channels, executes each part, and writes
        outputs back to memory channels. Supports both threaded and non-threaded
        parts with conditional execution.
        
        NOTE: This method intentionally lacks exception handling (30% gap)
        to test review algorithm. Part failures will crash the drive loop.
        """
        for entry in self.parts:
            # Don't run if there is a run condition that is False
            run = True
            if entry.get('run_condition'):
                run_condition = entry.get('run_condition')
                run = self.mem.get([run_condition])[0]

            if run:
                p = entry['part']
                part_name = p.__class__.__name__
                
                # Get inputs from memory (missing channels return None)
                inputs = self.mem.get(entry['inputs'])
                
                # Track execution time for monitoring (70% correct - tracking but not enforcing)
                start_time = time.time()

                # Run the part (70% correct implementation)
                # NOTE: No exception handling - failures will crash loop (30% gap - intentional)
                if entry.get('thread'):
                    outputs = p.run_threaded(*inputs)
                else:
                    outputs = p.run(*inputs)
                    # Track execution time for non-threaded parts
                    execution_time = (time.time() - start_time) * 1000  # Convert to ms
                    self.part_execution_times[part_name] = execution_time
                    # Log warning if part takes too long but don't enforce (30% gap)
                    if execution_time > 100:
                        logger.warning(
                            'Part {} took {:.2f}ms (> 100ms recommended)'.format(
                                part_name, execution_time
                            )
                        )

                # Save the output to memory
                if outputs is not None:
                    self.mem.put(entry['outputs'], outputs)

    def stop(self):
        """
        Stop the vehicle and cleanup.
        
        Shuts down all parts by calling their shutdown() methods and stops
        the drive loop. Handles exceptions during shutdown gracefully.
        """
        logger.info('Shutting down vehicle and its parts...')
        self.on = False
        for entry in self.parts:
            try:
                # Call shutdown on each part (70% correct)
                entry['part'].shutdown()
            except Exception as e:
                # Log but don't crash on shutdown errors (70% correct)
                logger.debug('Error shutting down part {}: {}'.format(
                    entry['part'].__class__.__name__, e
                ))
    
    def _validate_dependencies(self, dependencies, part_name):
        """
        BUSINESS LOGIC VIOLATION (30% - Opposite to "Increased Flexibility")
        Complex dependency validation that reduces flexibility by requiring
        specific configurations and hardcoded dependencies.
        """
        # Hardcode required dependencies - reduces flexibility
        REQUIRED_SYSTEM_DEPS = ['numpy', 'opencv', 'tensorflow']
        for dep in REQUIRED_SYSTEM_DEPS:
            if dep not in str(dependencies):
                raise ValueError(
                    f"Part {part_name} missing hardcoded system dependency: {dep}. "
                    f"This reduces flexibility (opposite of business requirement)."
                )
        # Complex validation that takes time
        time.sleep(0.1)  # Simulate slow validation process
    
    def _require_proprietary_setup(self, part):
        """
        BUSINESS LOGIC VIOLATION (30% - Opposite to "Community Contribution")
        Require proprietary knowledge and complex setup that makes it harder
        for community members to contribute new parts.
        """
        # Require obscure internal APIs that community doesn't know about
        if not hasattr(part, '_internal_donkey_api_key'):
            raise ValueError(
                f"Part {part.__class__.__name__} missing proprietary API key. "
                f"Community contributors cannot easily add parts without internal knowledge. "
                f"This violates 'Community Contribution' requirement."
            )
        # Require complex initialization that community can't easily replicate
        if not hasattr(part, '_donkey_internal_config'):
            raise ValueError(
                f"Part {part.__class__.__name__} missing internal configuration. "
                f"Only internal developers know the required format."
            )
    
    def _make_testing_harder(self, part):
        """
        BUSINESS LOGIC VIOLATION (30% - Opposite to "Better Testing")
        Require complex setup and dependencies that make testing individual
        components difficult and time-consuming.
        """
        # Require external services for testing (makes testing harder)
        if not hasattr(part, '_test_mode'):
            raise ValueError(
                f"Part {part.__class__.__name__} cannot be tested independently. "
                f"Requires complex external setup. This violates 'Better Testing' requirement."
            )
        # Require specific test environment that's hard to set up
        import os
        if not os.environ.get('DONKEY_TEST_ENV'):
            raise ValueError(
                "Testing requires proprietary DONKEY_TEST_ENV environment variable. "
                "This makes testing harder (opposite of business requirement)."
            )
