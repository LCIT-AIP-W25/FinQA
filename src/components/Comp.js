

import React, { useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const AccordionComponent = () => {
  const [expanded, setExpanded] = useState(false); // Track which accordion is expanded

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false); // Toggle state for the clicked accordion
  };

  return (
    <div>
      <Accordion
        expanded={expanded === 'panel1'}
        onChange={handleChange('panel1')}
        sx={{
          '& .MuiAccordionSummary-root': {
            backgroundColor: expanded === 'panel1' ? '#1976d2' : 'transparent',
            color: expanded === 'panel1' ? '#fff' : '#000',
            transition: 'background-color 0.3s ease', // Smooth transition
          },
        }}
      >
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Accordion 1</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Content for Accordion 1
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion
        expanded={expanded === 'panel2'}
        onChange={handleChange('panel2')}
        sx={{
          '& .MuiAccordionSummary-root': {
            backgroundColor: expanded === 'panel2' ? '#1976d2' : 'transparent',
            color: expanded === 'panel2' ? '#fff' : '#000',
            transition: 'background-color 0.3s ease',
          },
        }}
      >
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Accordion 2</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Content for Accordion 2
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion
        expanded={expanded === 'panel3'}
        onChange={handleChange('panel3')}
        sx={{
          '& .MuiAccordionSummary-root': {
            backgroundColor: expanded === 'panel3' ? '#1976d2' : 'transparent',
            color: expanded === 'panel3' ? '#fff' : '#000',
            transition: 'background-color 0.3s ease',
          },
        }}
      >
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Accordion 3</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            Content for Accordion 3
          </Typography>
        </AccordionDetails>
      </Accordion>
    </div>
  );
};

export default AccordionComponent;
