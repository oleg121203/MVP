# VentAI Enterprise Windsurf Configuration

This directory contains all Windsurf AI assistant configuration files for VentAI Enterprise.

## Directory Structure

```
.windsurf/
├── rules/          # AI assistant rules and protocols
├── activation/     # Activation commands and guides  
├── status/         # Status reports and monitoring
└── README.md       # This file
```

## Quick Start

### Primary Activation Command
```
VENTAI ENTERPRISE ACTIVATE
```

### Directory Contents

#### `/rules/` - AI Assistant Rules
Contains all Windsurf rules with priority hierarchy:
- **ABSOLUTE_MAXIMUM**: Error handling and bypass protocols
- **Maximum**: Anti-interruption and execution control
- **Critical**: Continuous execution rules
- **High/Medium**: Build automation and technical support

#### `/activation/` - Activation Commands
Contains activation guides and command references:
- Primary enterprise activation commands
- Emergency activation protocols
- General activation guides

#### `/status/` - Status Monitoring
Contains status reports and progress tracking:
- Enterprise implementation status
- Phase completion tracking
- Autoticket resolution status

## Configuration File

The main configuration is in the root `.windsurfrules` file, which references all rules in this directory structure.

## Usage

1. **Standard Operation**: Rules are automatically loaded
2. **Manual Activation**: Use commands from `/activation/`
3. **Status Check**: Review files in `/status/`
4. **Troubleshooting**: Reference specific rules in `/rules/`

## Maintenance

- All files are in English
- Follow naming conventions
- Maintain priority hierarchy
- Update paths when moving files

## Version

VentAI Enterprise Edition - Organized Structure v2.0